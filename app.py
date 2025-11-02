from flask import Flask
from flask import redirect, render_template, request, flash, make_response
from flask import session
from flask.helpers import abort
from werkzeug.security import generate_password_hash
import secrets
import src.db as db
import sqlite3

import src.users as users
import src.party as party

app = Flask(__name__)
# app.secret_key = secrets.token_hex(16)
app.secret_key = "18fd24bf6a2ad4dac04a33963db1c42f"


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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register_form.html")
    elif request.method == "POST":

        username = request.form["username"]
        displayname = request.form["displayname"]
        password1 = request.form["password"]
        password2 = request.form["password2"]
        if password1 != password2:
            return "VIRHE: salasanat eivät ole samat"
        password_hash = generate_password_hash(password1)

        try:
            sql = "INSERT INTO users (username, displayname, password_hash) VALUES (?, ?, ?)"
            db.execute(sql, [username, displayname, password_hash])
        except sqlite3.IntegrityError:
            flash("VIRHE: tunnus on jo varattu")
            return redirect("/register")

        flash("Tunnus luotu")
        return redirect("/")
    else:
        abort(make_response("Illegal method"))


@app.route("/create", methods=["GET", "POST"])
def create_party():
    if request.method == "GET":
        return render_template("create_form.html")
    elif request.method == "POST":
        users.require_login()
        users.check_csrf()

        title = request.form["title"]
        description = request.form["description"]
        start_date = request.form["start_date"]
        entry_fee = request.form["entry_fee"]
        sql = """INSERT INTO parties
        (title, description, start_date, entry_fee, user_id)
        VALUES (?, ?, ?, ?, ?)"""
        db.execute(sql, [title, description, start_date, entry_fee, session["user_id"]])

        return redirect(f"/party/{db.last_insert_id()}")
    else:
        abort(make_response("Illegal method"))


@app.route("/edit/<int:party_id>", methods=["GET", "POST"])
def edit_party(party_id: int):
    users.require_login()
    maybe_party = party.get_party(party_id)
    if maybe_party is None:
        abort(404)
    if maybe_party["organizer_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("edit_form.html", party=maybe_party)
    # elif method == "POST":
    users.check_csrf()
    title = request.form["title"]
    description = request.form["description"]
    start_date = request.form["start_date"]
    entry_fee = request.form["entry_fee"]
    try:
        party.edit_party(party_id, title, description, start_date, entry_fee)
        return redirect(f"/party/{party_id}")
    except ValueError as err:
        flash(str(err))
        abort(403)


@app.route("/delete/<int:party_id>")
def delete_party(party_id: int):
    return abort(404)


@app.route("/party/<int:party_id>")
def show_party(party_id: int):
    maybe_party = party.get_party(party_id)
    if maybe_party is not None:
        return render_template("party.html", party=maybe_party)
    else:
        return abort(404)


@app.route("/search/")
def search():
    query = request.args.get("query")
    if query is not None:
        parties = party.search_parties(query)
        return render_template("search_form.html", query=query, parties=parties)
    else:
        return render_template("search_form.html")


@app.route("/")
def index():
    parties = party.get_parties()
    return render_template("index.html", parties=parties)
