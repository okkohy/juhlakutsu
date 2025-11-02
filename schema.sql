CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , username TEXT UNIQUE
    , displayname TEXT NOT NULL
    , password_hash TEXT NOT NULL
);

CREATE TABLE parties (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , title TEXT NOT NULL
    , description TEXT
    , start_date DATETIME
    , entry_fee INTEGER
    , user_id INTEGER /* organizer id */
    /* if organizer is deleted, delete party */
    , CONSTRAINT fk_host_parties
      FOREIGN KEY (user_id)
      REFERENCES users(id)
      ON DELETE CASCADE
);

CREATE TABLE guests (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , party_id INTEGER
    , user_id INTEGER
    /* if the user or party is deleted, 
     delete the guest from guest list */
    , CONSTRAINT fk_user_parties
      FOREIGN KEY (user_id)
      REFERENCES users (id)
      ON DELETE CASCADE
    , CONSTRAINT fk_party_guests
      FOREIGN KEY (user_id)
      REFERENCES users (id)
      ON DELETE CASCADE
);


