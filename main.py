import pandas
import pandas as pd
import sqlite3
import sys
from pathlib import Path

from WeekClass import Week
from SqlLoader import create_db_table, load_data_into_db

temp_input_excel_path: Path = Path(r"palnext.xlsx")
temp_output_html_path: Path = Path(r"")
temp_sql_output_path: Path = Path(r"sqldb.db")


def main():
    generate_report(temp_input_excel_path, temp_output_html_path, temp_sql_output_path)


def generate_report(input_path: Path,
                    output_path: Path,
                    sql_output_path: Path
                    ):

    # Creates a dataframe object from the input Excel file
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

    output_path = output_path / f"Ugerapport {start_date} - {end_date}.html"

    # Saves the output file
    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write(weekly_report)

    close_db_connection(cursor, connection)


def create_dataframe(input_path: Path) -> pandas.DataFrame:
    # TODO: exceptions
    # noinspection PyTypeChecker
    df: pandas.DataFrame = pd.read_excel(input_path, usecols=[
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


def close_db_connection(cursor, connection):
    cursor.close()
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
