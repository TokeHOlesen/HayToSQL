import stylesheet
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from MainWIndowClass import MainWindow


def main():
    app = QApplication([])
    app.setStyleSheet(stylesheet.stylesheet)
    window = MainWindow()
    window.setWindowIcon(QIcon("report-icon.ico"))
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
