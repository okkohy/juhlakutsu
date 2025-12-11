from datetime import datetime, timedelta
from flask import session
from src import db

PARTIES_PER_PAGE = 21  # = 7 * 3


def party_count():
    sql = """
        SELECT COUNT (id)
        FROM parties
    """
    return db.query(sql)[0][0]


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
            LEFT JOIN categories ON party_categories.category_id = categories.id
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
            "start_date": parse_db_date(party_result[0][2]),
            "entry_fee": party_result[0][3],
            "organizer": party_result[0][7],
            "id": party_result[0][5],
            "guest_count": party_result[0][8],
            "organizer_id": party_result[0][6],
            "category": party_result[0][9],
            "category_id": party_result[0][10],
        }
        return party
    else:
        return None


def get_parties(page: int = 1):
    sql = """
    SELECT parties.id
    , parties.title
    , parties.description
    , parties.start_date
    , parties.entry_fee
    , parties.user_id
    , users.displayname
    , categories.name
    , COUNT (guests.id) guest_count
    FROM parties
    LEFT JOIN users ON parties.user_id = users.id
    LEFT JOIN party_categories ON parties.id = party_categories.party_id
    LEFT JOIN categories ON party_categories.category_id = categories.id
    LEFT JOIN guests ON parties.id = guests.party_id
    GROUP BY parties.id
    LIMIT ?
    OFFSET ?
    """
    offset = (page - 1) * PARTIES_PER_PAGE
    result = db.query(sql, [PARTIES_PER_PAGE, offset])
    parties = [
        {
            "id": party[0],
            "title": party[1],
            "description": party[2],
            "start_date": parse_db_date(party[3]),
            "entry_fee": party[4],
            "organizer_id": party[5],
            "organizer_displayname": party[6],
            "category": party[7],
            "guest_count": party[8],
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
    , categories.name
    , COUNT (guests.id)
    FROM guests all_guests
    JOIN parties ON parties.id = all_guests.party_id
    JOIN users ON parties.user_id = users.id
    LEFT JOIN party_categories ON parties.id = party_categories.party_id
    LEFT JOIN categories ON party_categories.category_id = categories.id
    LEFT JOIN guests ON parties.id = guests.party_id
    WHERE all_guests.user_id = ?
    GROUP BY parties.id
    """
    result = db.query(sql, [user_id])
    parties = [
        {
            "id": party[0],
            "title": party[1],
            "description": party[2],
            "start_date": parse_db_date(party[3]),
            "entry_fee": party[4],
            "organizer_id": party[5],
            "organizer_displayname": party[6],
            "category": party[7],
            "guest_count": party[8],
        }
        for party in result
    ]
    return parties


def create_party(title, description, start_date, entry_fee, category_id):
    start_date = parse_start_date(start_date)
    if entry_fee and len(entry_fee) > 0:
        entry_fee = int(entry_fee)

    if not 0 < len(title) < 50:
        raise ValueError(
            "VIRHE: Nimi on liian pitkä tai lyhyt. (Maksimi on 50 merkkiä)"
        )
    if not 0 < len(description) < 2000:
        raise ValueError(
            "VIRHE: Kuvaus on liian pitkä tai lyhyt. (Maksimi on 2000 merkkiä)"
        )
    if (
        not datetime.today() - timedelta(1)
        < start_date
        < datetime.today() + timedelta(365 * 5)
    ):
        raise ValueError("VIRHE: Valittu päivämäärä on liian kaukana nykyhetkestä.")
    if entry_fee:
        if not 0 < entry_fee < 1000:
            raise ValueError(f"VIRHE: Sisäänpääsymaksu ei ole kelpoinen {entry_fee}")

    sql = """INSERT INTO parties
    (title, description, start_date, entry_fee, user_id)
    VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, start_date, entry_fee, session["user_id"]])

    party_id = db.last_insert_id()
    if party_id:
        set_category(party_id, category_id)
    else:
        raise ValueError("VIRHE: Jotain meni pieleen")
    return party_id


def delete_party(party_id):
    sql = """
    DELETE FROM parties WHERE id = ?
    """
    db.execute(sql, [party_id])


def edit_party(party_id, new_title, new_description, new_start_date, new_entry_fee):
    # Data validation
    new_start_date = parse_start_date(new_start_date)
    if new_entry_fee is not None and len(new_entry_fee) > 0:
        new_entry_fee = int(new_entry_fee)

    if not 0 < len(new_title) < 50:
        raise ValueError(
            "VIRHE: Nimi on liian pitkä tai lyhyt. (Maksimi on 50 merkkiä)"
        )
    if not 0 < len(new_description) < 2000:
        raise ValueError(
            "VIRHE: Kuvaus on liian pitkä tai lyhyt. (Maksimi on 2000 merkkiä)"
        )
    if (
        not datetime.today() - timedelta(1)
        < new_start_date
        < datetime.today() + timedelta(365 * 5)
    ):
        raise ValueError("VIRHE: Valittu päivämäärä on liian kaukana nykyhetkestä")
    if new_entry_fee:
        if not 0 < new_entry_fee < 1000:
            raise ValueError(
                f"VIRHE: Sisäänpääsymaksu ei ole kelpoinen: {new_entry_fee}"
            )

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
    sql = """SELECT
             parties.id
             , parties.title
             , parties.description
             , parties.start_date
             , parties.entry_fee
             , parties.user_id
             , users.displayname
             , categories.name
             , COUNT (guests.id)
             FROM parties
             LEFT JOIN users ON parties.user_id = users.id
             LEFT JOIN party_categories ON parties.id = party_categories.party_id
             LEFT JOIN categories ON party_categories.category_id = categories.id
             LEFT JOIN guests ON parties.id = guests.party_id
             WHERE title LIKE ? OR description LIKE ?
             GROUP BY parties.id
             ORDER BY start_date ASC"""
    like = f"%{query}%"
    result = db.query(sql, [like, like])
    parties = [
        {
            "id": party[0],
            "title": party[1],
            "description": party[2],
            "start_date": parse_db_date(party[3]),
            "entry_fee": party[4],
            "organizer_id": party[5],
            "organizer_displayname": party[6],
            "category": party[7],
            "guest_count": party[8],
        }
        for party in result
        # sqlite doesn't know how to do date comparison
        # so have to do it like this
        if parse_db_date(party[3]) > datetime.today()
    ]
    return parties


def get_guests(party_id: int) -> list:
    sql = """
    SELECT
    guests.user_id
    , users.displayname
    FROM guests
    JOIN users ON guests.user_id = users.id
    WHERE party_id = ?
    """
    result = db.query(sql, [party_id])
    return [{"id": user[0], "displayname": user[1]} for user in result]


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
    return [{"id": category[0], "name": category[1]} for category in result]


def set_category(party_id: int, new_category_id: str | None) -> None:
    category_ids = [str(cat["id"]) for cat in get_categories()]
    if new_category_id and new_category_id in category_ids:
        category_id = int(new_category_id)
    else:
        return
    sql = """
    INSERT INTO party_categories (party_id, category_id) VALUES(?, ?)
    ON CONFLICT (party_id) DO UPDATE SET category_id = ?
    """
    db.execute(sql, [party_id, category_id, category_id])


def parse_db_date(start_date: str) -> datetime:
    return datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")


def parse_start_date(start_date: str) -> datetime:
    return datetime.strptime(start_date, "%Y-%m-%dT%H:%M")


def format_start_date(start_date: datetime, is_short: bool) -> str:
    if start_date.year == datetime.today().year and is_short:
        return start_date.strftime("%d.%m. %H.%M")
    elif is_short:
        return start_date.strftime("%d.%m.%Y")
    else:
        return start_date.strftime("%d.%m.%Y %H.%M")
