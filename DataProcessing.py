import pandas as pd
import sqlite3
import sys

from datetime import datetime
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal

from WeekClass import Week
from popup_messagebox import display_popup


class ReportGeneratorThread(QThread):
    finished = pyqtSignal()

    def __init__(self, input_path: Path, output_path: Path, keep_sql_file: bool):
        super().__init__()
        self.input_path: Path = input_path
        self.output_path: Path = output_path
        self.keep_sql_file = keep_sql_file

    def run(self):
        generate_and_save_report(self.input_path, self.output_path, self.keep_sql_file)
        self.finished.emit()


def generate_and_save_report(input_path: Path, output_path: Path, keep_sql_file: bool):

    # Sets the sql output path to the same directory as the html output
    sql_output_path = output_path.parent / "sqldb.db"

    # Creates a pandas dataframe object from the input Excel file
    df = create_dataframe(input_path)
    # Attempts to create an empty database file or clear an existing one
    connection, cursor = create_sqlite_db(sql_output_path)
    # Populates the database with data from the dataframe
    load_data_into_db(cursor, df)

    # Gets the dates of the first and last day in the database
    cursor.execute("SELECT MIN(date), MAX(date) FROM hay;")
    start_date, end_date = cursor.fetchall()[0]

    # Instantiates a Week object for the period covered in the database
    week: Week = Week(cursor, start_date, end_date)

    # Generates a string containing the report in HTML format
    weekly_report: str = week.generate_report()

    # Saves the output file
    try:
        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.write(weekly_report)
    except PermissionError:
        display_popup("Fejl", "Filen kan ikke skrives pga. manglede rettigheder.", "warning")
        return
    except OSError as e:
        display_popup("Fejl", f"Filen kan ikke skrives:\n{e}", "warning")
        return

    # Closes the connection to the database
    close_db_connection(cursor, connection)

    if not keep_sql_file:
        try:
            sql_output_path.unlink()
        except PermissionError:
            display_popup("Fejl", "SQL-filen kan ikke slettes - mangler rettigheder.", "warning")
        except Exception as e:
            display_popup("Fejl", f"Der er opstået en fejl ved sletning af databasefilen:\n{e}", "warning")


def create_dataframe(input_path: Path) -> pd.DataFrame:
    # TODO: exceptions
    # noinspection PyTypeChecker
    df: pd.DataFrame = pd.read_excel(input_path, usecols=[
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
    return df


def create_sqlite_db(sql_output_path: Path):
    if not sql_output_path.is_file():
        print("Advarsel: databasefilen findes ikke.\nForsøger at oprette en ny databasefil...", end="")
        try:
            with open(sql_output_path, "wb") as _:
                pass
            print("Færdig.")
        except OSError:
            print("Mislykket.")
            sys.exit(f'Fejl: kan ikke oprette "{sql_output_path.name}".')
    try:
        connection: sqlite3.Connection = sqlite3.connect(sql_output_path)
        cursor: sqlite3.Cursor = connection.cursor()
        create_db_table(cursor)
        return connection, cursor
    except sqlite3.OperationalError:
        sys.exit("Fejl: databasefilen findes, men indeholder ikke en gyldig tabel.")


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


def load_data_into_db(cursor: sqlite3.Cursor, df: pd.DataFrame) -> None:
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


def close_db_connection(cursor, connection):
    cursor.close()
    connection.commit()
    connection.close()
