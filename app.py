from flask import Flask, render_template
import src.db

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


@app.route("/")
def index():
    return render_template("index.html")
