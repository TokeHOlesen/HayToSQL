from PyQt6.QtWidgets import QApplication
from MainWIndowClass import MainWindow

# temp_input_excel_path: Path = Path(r"palnext.xlsx")
# temp_output_html_path: Path = Path(r"")
# temp_sql_output_path: Path = Path(r"sqldb.db")


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
