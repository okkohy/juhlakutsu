from flask import Flask
from flask import redirect, render_template, request
from werkzeug.security import generate_password_hash
import src.db as db
import sqlite3

app = Flask(__name__)


@app.route("/login_page")
def login_page():
    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def login():
    return "SUCCESS!"


@app.route("/register")
def register():
    return render_template("register_form.html")


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"


@app.route("/")
def index():
    return render_template("index.html")
