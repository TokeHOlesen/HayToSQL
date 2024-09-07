import pandas as pd
import sqlite3
import sys
from datetime import datetime, timedelta, date
from pathlib import Path

from OrderlineClass import Orderline
from DayClass import Day
from AlldaysClass import Alldays

# SQL_DB_PATH = Path(r"C:\Users\Toke Henrik Olesen\Code\PalissadeDB\sqldb.db")
SQL_DB_PATH = Path(r"sqldb.db")
EXCEL_FILE_PATH = Path(r"palcur.xlsx")


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
    
    all_days = get_orders_for_week(cursor, '2024-09-09', '2024-09-13')
    all_days.move_lines_to_match_date()
    all_days.calculate_kids_for_all_days()
    
    weekly_report = all_days.generate_weekly_report()
    
    with open("report.txt", "w",encoding="UTF-8-sig") as outfile:
        outfile.write(weekly_report)
    
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
    

def load_data_into_db(cursor, df):
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
                            datetime.strptime(str(df.loc[i, "Bekræftet leveringsdato"]), "%Y-%m-%d %H:%M:%S").isoformat(),
                            df.loc[i, "Konsoliderings ID"],
                            df.loc[i, "Leveringsnavn"],
                            df.loc[i, "Leveringsadresse"],
                            df.loc[i, "Leveringsby"],
                            df.loc[i, "Leveringspostnr."],
                            df.loc[i, "Leveringsland"],
                        ),
                    )


def get_orders_for_day(cursor, this_date):
    """
    Returns a list of Orderline objects for orders with the given shipping date.
    Includes orders with the same delivery address, even if they have a later shipping date, to make sure
    that orders get grouped together for delivery as much as possible.
    """
    if not isinstance(this_date, date):
        this_date = datetime.strptime(date, r"%Y-%m-%d").date()
    day = Day(this_date)
    cursor.execute("""SELECT * FROM hay
                   WHERE address IN (SELECT address FROM hay GROUP BY address HAVING MIN(date) = ?)
                   AND location IS NOT 'DSV';""", (this_date,))
    result = cursor.fetchone()
    while result is not None:
        day.add_line(Orderline(result))
        result = cursor.fetchone()
    return day


def get_orders_for_week(cursor, start_date, end_date):
    start_date = datetime.strptime(start_date, r"%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, r"%Y-%m-%d").date()
    all_days = Alldays()
    for i in range((end_date - start_date).days + 1):
        all_days.add_day(get_orders_for_day(cursor, (start_date + timedelta(days=i))))
    return all_days
    
 
if __name__ == "__main__":
    main()

# 