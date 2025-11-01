CREATE TABLE users (
    id INTEGER PRIMARY KEY
    , username TEXT UNIQUE
    , displayname TEXT NOT NULL
    , password_hash TEXT NOT NULL
);

CREATE TABLE parties (
    id INTEGER PRIMARY KEY
    , title TEXT NOT NULL
    , description TEXT
    , start_date DATETIME
    , entry_fee INTEGER
    , user_id INTEGER REFERENCES users /* organizer id */
);

CREATE TABLE guests (
    id INTEGER PRIMARY KEY
    , party_id INTEGER REFERENCES parties
    , user_id INTEGER REFERENCES users
);


