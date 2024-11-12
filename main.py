import stylesheet
from PyQt6.QtWidgets import QApplication
from MainWIndowClass import MainWindow


def main():
    app = QApplication([])
    app.setStyleSheet(stylesheet.stylesheet)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
