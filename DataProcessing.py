import pandas as pd
import sqlite3

from datetime import datetime
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal

from WeekClass import Week
from popup_messagebox import display_popup


class ReportGeneratorThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, input_path: Path, output_path: Path, keep_sql_file: bool):
        super().__init__()
        self.input_path: Path = input_path
        self.output_path: Path = output_path
        self.keep_sql_file = keep_sql_file

    def run(self):
        try:
            generate_and_save_report(self.input_path, self.output_path, self.keep_sql_file)
        except Exception as e:
            self.error.emit(str(e))
        else:
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
    # Checks if both the start date and the end date in the input file fall in the same week
    if week.start_date.isocalendar()[:2] != week.end_date.isocalendar()[:2]:
        close_db_connection(cursor, connection)
        delete_sql_file(sql_output_path)
        raise RuntimeError(
            f"Inputfilen skal omfatte en periode på højst en uge, og både start- og slutdatoen skal ligge i samme uge."
            f"\n\nDen valgte fil har startdato d. {week.start_date} og slutdato d. {week.end_date}.")
    # Generates a string containing the report in HTML format
    weekly_report: str = week.generate_report()
    # Saves the output file. Raises an exception if the file can't be written,
    # and closes the database connection if it has been established
    try:
        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.write(weekly_report)
    except PermissionError:
        raise RuntimeError("Rapportfilen kan ikke skrives pga. manglede rettigheder.")
    except OSError as e:
        raise RuntimeError(f"Rapportfilen kan ikke skrives:\n\n{e}")
    finally:
        if "cursor" in locals():
            close_db_connection(cursor, connection)

    if not keep_sql_file:
        delete_sql_file(sql_output_path)


def delete_sql_file(sql_output_path: Path):
    try:
        sql_output_path.unlink()
    except PermissionError:
        display_popup("Fejl", "SQL-filen kan ikke slettes - mangler rettigheder.", "warning")
    except Exception as e:
        display_popup("Fejl", f"Der er opstået en fejl ved sletning af databasefilen:\n\n{e}", "warning")


def create_dataframe(input_path: Path) -> pd.DataFrame:
    try:
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
    except PermissionError:
        raise RuntimeError("Excel-filen kan ikke læses - mangler rettigheder.")
    except pd.errors.EmptyDataError:
        raise RuntimeError("Excel-filen er tom eller indeholder ikke de nødvendige data.")
    except ValueError:
        raise RuntimeError("Inputfilen er ikke en Excel-fil eller mangler de nødvendige data.")
    return df


def create_sqlite_db(sql_output_path: Path):
    # Attempts to create an empty file for the database. Overwrites any existing files.
    try:
        with open(sql_output_path, "wb") as _:
            pass
    except PermissionError:
        raise RuntimeError("Databasefilen kan ikke skrives - mangler rettigheder.")
    except OSError:
        raise RuntimeError("Databasefilen kan ikke skrives.")
    # Attempts to create a table in the newly created file. Returns cursor and connection objects.
    try:
        connection: sqlite3.Connection = sqlite3.connect(sql_output_path)
        cursor: sqlite3.Cursor = connection.cursor()
        create_db_table(cursor)
        return connection, cursor
    except (sqlite3.OperationalError, sqlite3.IntegrityError, sqlite3.DatabaseError) as e:
        raise RuntimeError(f"Databasen kan ikke oprettes:\n\n{e}")


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
    try:
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
    except (KeyError,
            ValueError,
            TypeError,
            sqlite3.OperationalError,
            sqlite3.IntegrityError,
            sqlite3.DatabaseError) as e:
        raise RuntimeError(f"Der er opstået en fejl ved indlæsning af data:\n\n{e}")
    except Exception as e:
        raise RuntimeError(f"Der er opstået en fejl:\n\n{e}")


def close_db_connection(cursor, connection):
    cursor.close()
    connection.commit()
    connection.close()
