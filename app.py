from datetime import datetime, timedelta
import time
import math
import sqlite3
import secrets
import markupsafe
from flask import Flask
from flask import redirect, render_template, request, flash, make_response
from flask import session, g
from flask.helpers import abort
import src.db as db

import src.users as users
import src.party as party

app = Flask(__name__)
# app.secret_key = secrets.token_hex(16)
app.secret_key = "18fd24bf6a2ad4dac04a33963db1c42f"

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br>")
    return markupsafe.Markup(content)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_form.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            result = db.query(
                "SELECT displayname FROM users WHERE username = ?", [username]
            )
            displayname = result[0][0]
            session["displayname"] = displayname
            session["csrf_token"] = secrets.token_hex(16)
            # Success
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")
    else:
        abort(make_response("Illegal method"))


@app.route("/logout")
def logout():
    if "user_id" in session:
        session.pop("user_id")
        session.pop("username")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register_form.html")
    elif request.method == "POST":

        username = request.form["username"]
        displayname = request.form["displayname"]
        password1 = request.form["password"]
        password2 = request.form["password2"]

        try:
            users.create_user(username, displayname, password1, password2)
        except sqlite3.IntegrityError:
            flash("VIRHE: tunnus on jo varattu")
            return redirect("/register")
        except ValueError as er:
            flash(str(er))
            return redirect("/register")

        flash("Tunnus luotu")
        return redirect("/")
    else:
        abort(make_response("Illegal method"))


@app.route("/create", methods=["GET", "POST"])
def create_party():
    if request.method == "GET":
        categories = party.get_categories()
        yesterday = datetime.today().date().strftime("%Y-%m-%dT%H:%M")
        max_date = (datetime.today().date() + timedelta(365 * 5)).strftime(
            "%Y-%m-%dT%H:%M"
        )
        return render_template(
            "create_form.html",
            categories=categories,
            yesterday=yesterday,
            max_date=max_date,
        )
    elif request.method == "POST":
        users.require_login()
        users.check_csrf()

        title = request.form["title"]
        description = request.form["description"]
        start_date = request.form["start_date"]
        entry_fee = request.form["entry_fee"]
        category_id = request.form["category"]
        try:
            party_id = party.create_party(
                title, description, start_date, entry_fee, category_id
            )
        except ValueError as err:
            flash(str(err))
            return redirect("/create")

        return redirect(f"/party/{party_id}")
    else:
        abort(make_response("Illegal method"))


@app.route("/edit/<int:party_id>", methods=["GET", "POST"])
def edit_party(party_id: int):
    users.require_login()
    maybe_party = party.get_party(party_id)
    categories = party.get_categories()
    yesterday = datetime.today().date().strftime("%Y-%m-%dT%H:%M")
    max_date = (datetime.today().date() + timedelta(365 * 5)).strftime("%Y-%m-%dT%H:%M")
    if maybe_party is None:
        return abort(404)
    if maybe_party["organizer_id"] != session["user_id"]:
        return abort(403)
    # Filter out the category that is currently selected
    categories = [cat for cat in categories if cat["id"] != maybe_party["category_id"]]
    if request.method == "GET":
        return render_template(
            "edit_form.html",
            party=maybe_party,
            categories=categories,
            yesterday=yesterday,
            max_date=max_date,
        )
    # elif method == "POST":
    users.check_csrf()
    title = request.form["title"]
    description = request.form["description"]
    start_date = request.form["start_date"]
    entry_fee = request.form["entry_fee"]
    new_category = request.form["category"]
    try:
        party.edit_party(party_id, title, description, start_date, entry_fee)
        party.set_category(party_id, new_category)
        return redirect(f"/party/{party_id}")
    except ValueError as err:
        flash(str(err))
        return redirect(f"/edit/{party_id}")


@app.route("/delete/<int:party_id>", methods=["GET", "POST"])
def delete_party(party_id: int):
    users.require_login()
    maybe_party = party.get_party(party_id)

    if maybe_party is not None:
        if session["user_id"] != maybe_party["organizer_id"]:
            return abort(403)
    else:
        return abort(404)

    if request.method == "GET":
        return render_template("delete_form.html", party=maybe_party)

    # else mehtod == "POST"
    users.check_csrf()
    if "remove" in request.form:
        party.delete_party(party_id)
        flash("Juhla poistettu")
        return redirect("/")
    else:
        return redirect(f"/edit/{party_id}")


@app.route("/attend/<int:party_id>", methods=["POST"])
def attend(party_id: int):
    users.require_login()
    users.check_csrf()
    maybe_party = party.get_party(party_id)

    if maybe_party is None:
        return abort(404)

    if "attend" in request.form:
        party.add_guest(party_id, session["user_id"])
        flash("Ilmottautuminen hyväksytty.")
        return redirect(f"/party/{party_id}")
    else:
        flash("Ilmottautuminen peruttu.")
        party.remove_guest(party_id, session["user_id"])
        return redirect(f"/party/{party_id}")


@app.route("/party/<int:party_id>")
def show_party(party_id: int):
    maybe_party = party.get_party(party_id)
    guests = party.get_guests(party_id)

    current_user_id = session.get("user_id")

    current_user_is_guest = (
        guests is not None
        and current_user_id is not None
        and len(guests) != 0
        and current_user_id in [guest["id"] for guest in guests]
    )
    if maybe_party is not None:
        start_date = maybe_party["start_date"]
        maybe_party["start_date"] = party.format_start_date(start_date, False)
        return render_template(
            "party.html",
            party=maybe_party,
            is_guest=current_user_is_guest,
            attendees=guests,
        )
    else:
        return abort(404)


@app.route("/user/<int:user_id>")
def show_user(user_id: int):
    maybe_user = users.get_user(user_id)
    parties = users.get_parties(user_id)
    attended_parties = party.get_attended(user_id)

    current_user_id = session.get("user_id")

    party_count = len(parties)
    attend_count = len(attended_parties)

    for p in parties:
        start_date = p["start_date"]
        p["start_date"] = party.format_start_date(start_date, True)
    for a in attended_parties:
        start_date = a["start_date"]
        a["start_date"] = party.format_start_date(start_date, True)

    if maybe_user is not None:
        return render_template(
            "user.html",
            user=maybe_user,
            parties=parties,
            attended=attended_parties,
            party_count=party_count,
            attend_count=attend_count,
        )
    else:
        return abort(404)


@app.route("/search/")
def search():
    query = request.args.get("query")
    if query is not None:
        parties = party.search_parties(query)
        for p in parties:
            start_date = p["start_date"]
            p["start_date"] = party.format_start_date(start_date, True)
        return render_template("search_form.html", query=query, parties=parties)
    else:
        return render_template("search_form.html")


@app.route("/")
@app.route("/<int:page>")
def index(page: int = 1):
    if page < 1:
        return redirect("/")

    party_count = party.party_count()
    parties = party.get_parties(page)
    page_count = max(1, math.ceil(party_count / party.PARTIES_PER_PAGE))

    if page_count < page:
        return redirect(f"/{page_count}")
    for p in parties:
        start_date = p["start_date"]
        p["start_date"] = party.format_start_date(start_date, True)
    return render_template(
        "index.html", parties=parties, page=page, page_count=page_count
    )
