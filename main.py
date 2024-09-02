import pandas as pd
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

SQL_DB_PATH = Path(r"C:\Users\Toke Henrik Olesen\Code\PalissadeDB\sqldb.db")
EXCEL_FILE_PATH = Path(r"paltestr.xlsx")

def main():
    # TODO: exceptions
    df = pd.read_excel(EXCEL_FILE_PATH, usecols=[
    "Plukserie (ordrelinje)",
    "Varenummer",
    "Beskrivelse",
    "Antal3",
    "Beregnet ladmeter",
    "Bekræftet leveringsdato",
    "Leveringsnavn",
    "Leveringsadresse",
    "Leveringsby",
    "Leveringspostnr.",
    "Leveringsland",
    "Description 2",
    "Hay KO-no.",
    "Hay Lokation",
    "Konsoliderings ID"
    ])
    
    if not SQL_DB_PATH.is_file():
        print("Advarsel: databasefilen findes ikke.\nForsøger at oprette en ny databasefil...", end="")
        try:
            with open(SQL_DB_PATH, "wb") as _:
                pass
            print("Færdig.")
        except OSError:
            print("Mislykket.")
            sys.exit(f'Fejl: kan ikke oprette "{SQL_DB_PATH.name}".')
    try:
        connection = sqlite3.connect(SQL_DB_PATH)
        cursor = connection.cursor()
        create_db_table(cursor)
    except sqlite3.OperationalError:
        sys.exit("Fejl: databasefilen findes, men indeholder ikke en gyldig tabel.")
    
    load_data_into_db(cursor, df)
    
    cursor.close()
    connection.commit()
    connection.close()


def create_db_table(cursor):
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS hay (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ordernumber TEXT NOT NULL,
        pickseries TEXT,
        location TEXT,
        itemnumber TEXT,
        itemname TEXT,
        itemcolor TEXT,
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
    

def load_data_into_db(cursor, df):
    cursor.execute("DELETE FROM hay;")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='hay';")
    for i in range(df.shape[0]):
        cursor.execute(
                        "INSERT INTO hay (ordernumber, pickseries, location, itemnumber, itemname, itemcolor, number,"
                        "loadmeter, date, kid, custname, address, city, postcode, country) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                        (
                            df.loc[i, "Hay KO-no."],
                            df.loc[i, "Plukserie (ordrelinje)"],
                            df.loc[i, "Hay Lokation"],
                            df.loc[i, "Varenummer"],
                            df.loc[i, "Beskrivelse"],
                            df.loc[i, "Description 2"],
                            int(df.loc[i, "Antal3"]),
                            df.loc[i, "Beregnet ladmeter"],
                            str(df.loc[i, "Bekræftet leveringsdato"]),
                            df.loc[i, "Konsoliderings ID"],
                            df.loc[i, "Leveringsnavn"],
                            df.loc[i, "Leveringsadresse"],
                            df.loc[i, "Leveringsby"],
                            df.loc[i, "Leveringspostnr."],
                            df.loc[i, "Leveringsland"],
                        ),
                    )
    

if __name__ == "__main__":
    main()
