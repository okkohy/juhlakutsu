from flask import Flask
from flask import redirect, render_template, request, flash, make_response
from flask import session
from flask.helpers import abort
from werkzeug.security import generate_password_hash
import secrets
import src.db as db
import sqlite3

import src.users as users

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
        result = db.query(
            "SELECT displayname FROM users WHERE username = ?", [username]
        )
        displayname = result[0][0]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["displayname"] = displayname
            session["csrf_token"] = secrets.token_hex(16)
            # Success
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")
    else:
        abort(make_response("Illegal method"))


@app.route("/register", methods=["POST", "GET"])
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


@app.route("/create", methods=["POST", "GET"])
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


@app.route("/party/<int:party_id>")
def show_party(party_id: int):
    sql = """SELECT
            parties.title
            , parties.description
            , parties.start_date
            , parties.entry_fee
            , parties.user_id
            , parties.id
            , users.id
            , users.displayname
            , COUNT (guests.id) guest_count
            FROM parties JOIN users ON parties.user_id = users.id
            LEFT JOIN guests ON parties.id = guests.party_id
            WHERE parties.id = ?"""
    party_result = db.query(sql, [party_id])
    if party_result is not None:
        party = {
            "title": party_result[0][0],
            "description": party_result[0][1],
            "start_date": party_result[0][2],
            "entry_fee": party_result[0][3],
            "organizer": party_result[0][7],
            "id": party_result[0][5],
            "guest_count": party_result[0][8],
            "organizer_id": party_result[0][5],
        }
        return render_template("party.html", party=party)
    else:
        return abort(404)


@app.route("/")
def index():
    sql = """
    SELECT parties.id
    , parties.title
    , parties.description
    , parties.start_date
    , parties.entry_fee
    , parties.user_id
    , users.displayname
    FROM parties LEFT JOIN users ON parties.user_id = users.id
    """
    result = db.query(sql, [])
    parties = [
        {
            "id": party[0],
            "title": party[1],
            "description": party[2],
            "start_date": party[3],
            "entry_fee": party[4],
            "organizer_id": party[5],
            "organizer_displayname": party[6],
        }
        for party in result
    ]
    return render_template("index.html", parties=parties)
