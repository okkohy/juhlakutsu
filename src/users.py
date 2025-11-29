from werkzeug.security import check_password_hash, generate_password_hash
from flask import session, request, abort
import src.db as db
import src.party as fest


def get_user(user_id: int) -> dict | None:
    sql = """
    SELECT username, displayname
    FROM users WHERE id = ?
    """
    result = db.query(sql, [user_id])
    if result:
        return {
            "username": result[0][0],
            "displayname": result[0][1],
        }


def create_user(username, displayname, password1, password2):
    if password1 != password2:
        raise ValueError("VIRHE: salasanat eivät ole samat")
    if not 0 < len(username) <= 30:
        raise ValueError("Käyttäjätunnuksen täytyy olla 1-30 merkkiä")
    if not 0 < len(displayname) <= 30:
        raise ValueError("Kutsumanimen täytyy olla 1-30 merkkiä")
    if not 10 <= len(password1) <= 200:
        raise ValueError("Salasanan täytyy olla 10-200 merkkiä")

    password_hash = generate_password_hash(password1)
    sql = "INSERT INTO users (username, displayname, password_hash) VALUES (?, ?, ?)"
    db.execute(sql, [username, displayname, password_hash])


def get_parties(user_id):
    sql = """
    SELECT parties.id
    , parties.title
    , parties.description
    , parties.start_date
    , parties.entry_fee
    , parties.user_id
    FROM parties
    WHERE parties.user_id = ?
    """
    result = db.query(sql, [user_id])
    parties = [
        {
            "id": party[0],
            "title": party[1],
            "description": party[2],
            "start_date": fest.parse_db_date(party[3]),
            "entry_fee": party[4],
            "organizer_id": party[5],
        }
        for party in result
    ]
    return parties


def check_login(username: str, password: str) -> int | None:
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None


def require_login():
    if "user_id" not in session:
        abort(403)


def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)
