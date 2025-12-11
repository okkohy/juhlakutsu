import random
import secrets
import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM parties")

user_count = 1000
party_count = 10**5
attendee_count = 10**6
category_count = 9

for i in range(1, user_count + 1):
    p = secrets.token_hex(12)
    password = generate_password_hash(p)
    displayname = f"user_d_{i}"
    username = "user" + str(i)
    if i == 1:
        print(f"user: {username}, pass={p}")
    db.execute("INSERT INTO users (username, displayname, password_hash) VALUES (?, ?, ?)",
               [username, displayname, password])

for i in range(1, party_count + 1):
    entry_fee = random.randint(0, 20)
    title = f"Juhlat {i}"
    description = f"Juhlien {i} kuvaus tässä näin"
    today = datetime.today()
    td = today.date()
    year = td.year
    month = td.month
    day = td.day
    hour = today.hour
    minute = today.minute
    start_date = (datetime(year, month, day, hour, minute) + timedelta(i % 365))
    user_id = random.randint(1, user_count)
    db.execute("INSERT INTO parties (title, description, start_date, entry_fee, user_id) VALUES (?,?,?,?,?)",
               [title, description, start_date, entry_fee, user_id])

for i in range(1, attendee_count + 1):
    user_id = random.randint(1, user_count)
    party_id = random.randint(1, party_count)
    db.execute("""INSERT INTO guests (party_id, user_id)
                  VALUES (?, ?)""",
               [party_id, user_id])

for i in range(1, party_count + 1):
    category_id = random.randint(0,9)
    if category_count != 0:
        db.execute("""INSERT INTO party_categories(party_id, category_id) VALUES (?, ?)""", [i, category_id])

db.commit()
db.close()
