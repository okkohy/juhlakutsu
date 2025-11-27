import src.db as db
from datetime import datetime, timedelta
from flask import session


def get_party(party_id: int) -> dict | None:
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
            , categories.name
            , categories.id
            FROM parties JOIN users ON parties.user_id = users.id
            LEFT JOIN guests ON parties.id = guests.party_id
            LEFT JOIN party_categories ON parties.id = party_categories.party_id
            JOIN categories ON party_categories.category_id = categories.id
            WHERE parties.id = ?"""
    party_result = db.query(sql, [party_id])
    if party_result is not None and len(party_result) != 0:
        if party_result[0][0] is None:
            # because we use COUNT the object is non null
            # but has fields None except guest_count = 0
            # so we have to do this extra check so we can correctly
            # return a 404
            return None
        party = {
            "title": party_result[0][0],
            "description": party_result[0][1],
            "start_date": party_result[0][2],
            "entry_fee": party_result[0][3],
            "organizer": party_result[0][7],
            "id": party_result[0][5],
            "guest_count": party_result[0][8],
            "organizer_id": party_result[0][6],
            "category": party_result[0][9],
            "category_id": party_result[0][10],
        }
        return party


def get_parties():
    sql = """
    SELECT parties.id
    , parties.title
    , parties.description
    , parties.start_date
    , parties.entry_fee
    , parties.user_id
    , users.displayname
    , categories.name
    FROM parties
    LEFT JOIN users ON parties.user_id = users.id
    LEFT JOIN party_categories ON parties.id = party_categories.party_id
    JOIN categories ON party_categories.category_id = categories.id
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
            "category": party[7],
        }
        for party in result
    ]
    return parties


def get_attended(user_id):
    sql = """
    SELECT parties.id
    , parties.title
    , parties.description
    , parties.start_date
    , parties.entry_fee
    , parties.user_id
    , users.displayname
    FROM parties RIGHT JOIN guests ON parties.id = guests.party_id
    LEFT JOIN users ON parties.user_id = users.id
    WHERE guests.user_id = ?
    """
    result = db.query(sql, [user_id])
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
    return parties


def create_party(title, description, start_date, entry_fee, category_id):
    start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
    entry_fee = int(entry_fee)

    if not 0 < len(title) < 50:
        raise ValueError("Nimi on liian pitkä tai lyhyt")
    if not 0 < len(description) < 2000:
        raise ValueError("Kuvaus on liian pitkä tai lyhyt")
    if not datetime.today() - timedelta(1) < start_date < datetime.today() + timedelta(365*5):
        raise ValueError("Valittu päivämäärä on liian kaukana nykyhetkestä")
    if not 0 < entry_fee < 1000:
        raise ValueError("Sisäänpääsymaksu ei ole kelpoinen")

    sql = """INSERT INTO parties
    (title, description, start_date, entry_fee, user_id)
    VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, start_date, entry_fee, session["user_id"]])

    if category_id:
        sql = """
        INSERT INTO party_categories(party_id, category_id) VALUES (?,?)
        """
        party_id = db.last_insert_id()
        db.execute(sql, [party_id, int(category_id)])

def delete_party(party_id):
    sql = """
    DELETE FROM parties WHERE id = ?
    """
    db.execute(sql, [party_id])


def edit_party(party_id, new_title, new_description, new_start_date, new_entry_fee):
    # Data validation
    new_start_date = datetime.strptime(new_start_date, "%Y-%m-%dT%H:%M")
    new_entry_fee = int(new_entry_fee)
    if not 0 < len(new_title) < 50:
        raise ValueError("Nimi on liian pitkä tai lyhyt")
    if not 0 < len(new_description) < 2000:
        raise ValueError("Kuvaus on liian pitkä tai lyhyt")
    if not datetime.today() - timedelta(1) < new_start_date < datetime.today() + timedelta(365*5):
        raise ValueError("Valittu päivämäärä on liian kaukana nykyhetkestä")
    if not 0 < new_entry_fee < 1000:
        raise ValueError("Sisäänpääsymaksu ei ole kelpoinen: {}")
    # Now everything should be ok
    sql = """
    UPDATE parties SET
    title = ?
    , description = ?
    , start_date = ?
    , entry_fee = ?
    WHERE id = ?
    """
    db.execute(
        sql, [new_title, new_description, new_start_date, new_entry_fee, party_id]
    )


def search_parties(query: str) -> list:
    # ORDER BY ASC makes sure that the parties
    # get shown such that the party that will start
    # soonest will be first
    # TODO: Filter parties where today > start_date
    sql = """SELECT
             parties.id
             , parties.title
             , parties.description
             , parties.start_date
             , parties.entry_fee
             , parties.user_id
             , users.displayname
             , categories.name
             FROM parties
             LEFT JOIN users ON parties.user_id = users.id
             LEFT JOIN party_categories ON parties.id = party_categories.party_id
             JOIN categories ON party_categories.category_id = categories.id
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY start_date ASC"""
    like = f"%{query}%"
    result = db.query(sql, [like, like])
    parties = [
        {
            "id": party[0],
            "title": party[1],
            "description": party[2],
            "start_date": party[3],
            "entry_fee": party[4],
            "organizer_id": party[5],
            "organizer_displayname": party[6],
            "category": party[7],
        }
        for party in result
    ]
    return parties


def get_guests(party_id: int) -> list:
    sql = """
    SELECT user_id FROM guests WHERE party_id = ?
    """
    return db.query(sql, [party_id])


def add_guest(party_id: int, user_id: int) -> None:
    sql = """
        SELECT party_id, user_id
        FROM guests WHERE party_id = ? AND user_id = ?
    """
    result = db.query(sql, [party_id, user_id])
    if len(result) == 0:
        sql = """
        INSERT INTO guests (party_id, user_id) VALUES (?, ?)
        """
        db.execute(sql, [party_id, user_id])


def remove_guest(party_id: int, user_id: int) -> None:
    sql = """
    DELETE FROM guests WHERE party_id = ? AND user_id = ?
    """
    db.execute(sql, [party_id, user_id])


def get_categories() -> list:
    sql = """
    SELECT id, name FROM categories ORDER BY id
    """
    result = db.query(sql)
    return [{
            "id": category[0],
            "name": category[1]
        }
        for category in result
    ]


def add_category(party_id: int, category_id: int) -> None:
    sql = """
    INSERT INTO party_categories (party_id, category_id) VALUES (?, ?)
    """
    db.execute(sql, [party_id, category_id])


def edit_category(party_id: int, new_category_id: int) -> None:
    sql = """
    UPDATE party_categories SET category_id = ? WHERE party_id = ?
    """
    db.execute(sql, [new_category_id, party_id])
