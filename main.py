import pandas
import pandas as pd
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

from WeekClass import Week

SQL_DB_PATH: Path = Path(r"sqldb.db")
EXCEL_FILE_PATH: Path = Path(r"pal16-20.xlsx")


def main():
    # TODO: exceptions
    # noinspection PyTypeChecker
    df: pandas.DataFrame = pd.read_excel(EXCEL_FILE_PATH, usecols=[
        "Plukserie (ordrelinje)",
        "Varenummer", "Beskrivelse",
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
        connection: sqlite3.Connection = sqlite3.connect(SQL_DB_PATH)
        cursor: sqlite3.Cursor = connection.cursor()
        create_db_table(cursor)
    except sqlite3.OperationalError:
        sys.exit("Fejl: databasefilen findes, men indeholder ikke en gyldig tabel.")
    
    load_data_into_db(cursor, df)

    cursor.execute("SELECT MIN(date), MAX(date) FROM hay;")
    start_date: str
    end_date: str
    start_date, end_date = cursor.fetchall()[0]
    
    week: Week = Week(cursor, start_date, end_date)
    
    weekly_report: str = week.generate_report()

    with open("report.html", "w", encoding="UTF-8") as outfile:
        outfile.write(weekly_report)

    cursor.close()
    connection.commit()
    connection.close()


def create_db_table(cursor: sqlite3.Cursor) -> None:
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

 
if __name__ == "__main__":
    main()
