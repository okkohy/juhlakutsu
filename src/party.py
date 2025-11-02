import src.db as db


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
            FROM parties JOIN users ON parties.user_id = users.id
            LEFT JOIN guests ON parties.id = guests.party_id
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
    return parties


def delete_party(party_id):
    sql = """
    DELETE FROM parties WHERE id = ?
    """
    db.execute(sql, [party_id])

def edit_party(party_id, new_title, new_description, new_start_date, new_entry_fee):
    # Data validation
    if len(new_title) > 50:
        raise ValueError("Nimi on liian pitkä")
    if len(new_description) > 2000:
        raise ValueError("Kuvaus on liian pitkä")
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
             FROM parties
             LEFT JOIN users ON parties.user_id = users.id
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
        }
        for party in result
    ]
    return parties
