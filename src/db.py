import sqlite3
from typing import Any
from flask import g


def get_connection() -> sqlite3.Connection:
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con


def execute(sql: str, params=[]) -> None:
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()


def last_insert_id() -> int | None:
    return g.last_insert_id


def query(sql: str, params=[]) -> list[Any]:
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
