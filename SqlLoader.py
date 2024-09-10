import pandas
import sqlite3

from datetime import datetime


def create_db_table(cursor: sqlite3.Cursor) -> None:
    """Creates an SQLite3 table, with fields matching those of an Orderline object."""
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS hay (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ordernumber TEXT NOT NULL,
        pickseries TEXT,
        location TEXT,
        itemnumber TEXT,
        itemname TEXT,
        color TEXT,
        number INTEGER,
        loadmeter REAL,
        date TEXT,
        kid TEXT,
        custname TEXT,
        address TEXT,
        city TEXT,
        postcode TEXT,
        country TEXT
        );"""
    )


def load_data_into_db(cursor: sqlite3.Cursor, df: pandas.DataFrame) -> None:
    cursor.execute("DELETE FROM hay;")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='hay';")
    for i in range(df.shape[0]):
        cursor.execute(
            "INSERT INTO hay (ordernumber, pickseries, location, itemnumber, itemname, color, number,"
            "loadmeter, date, kid, custname, address, city, postcode, country) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, DATE(?), ?, ?, ?, ?, ?, ?);",
            (
                df.loc[i, "Hay KO-no."],
                df.loc[i, "Plukserie (ordrelinje)"],
                df.loc[i, "Hay Lokation"],
                df.loc[i, "Varenummer"],
                df.loc[i, "Beskrivelse"],
                df.loc[i, "Description 2"],
                int(df.loc[i, "Antal3"]),
                df.loc[i, "Beregnet ladmeter"],
                datetime.strptime(str(df.loc[i, "Bekræftet leveringsdato"]),
                                  "%Y-%m-%d %H:%M:%S").isoformat(),
                df.loc[i, "Konsoliderings ID"],
                df.loc[i, "Leveringsnavn"],
                df.loc[i, "Leveringsadresse"],
                df.loc[i, "Leveringsby"],
                df.loc[i, "Leveringspostnr."],
                df.loc[i, "Leveringsland"],
            ),
        )
