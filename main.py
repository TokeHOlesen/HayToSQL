import pandas
import pandas as pd
import sqlite3
import sys
from pathlib import Path

from WeekClass import Week
from SqlLoader import create_db_table, load_data_into_db

SQL_DB_PATH: Path = Path(r"sqldb.db")
EXCEL_FILE_PATH: Path = Path(r"palcur.xlsx")


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

    with open("report.html", "w", encoding="utf-8") as outfile:
        outfile.write(weekly_report)

    cursor.close()
    connection.commit()
    connection.close()

 
if __name__ == "__main__":
    main()
