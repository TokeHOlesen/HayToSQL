import stylesheet
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from MainWIndowClass import MainWindow


# ** GENERAL OVERVIEW **
#
# The code accepts an Excel file exported from NAV as input and generates an HTML file as output.
# The Excel file is converted into a Pandas dataframe, which is then used as a data source for an SQLite database.
# Data is read from the database and a string containing the report is generated.
# Optionally, the file containing the database can be saved as well (same output path as the report).
#
# The data for the orders stored in the Excel file is used to instantiate Orderline objects, which contain only the data
# relevant to the report (as properties). Each Orderline object corresponds directly to a line in NAV.
#
# Orderlines are grouped together to form Day objects, which contain all the orderlines that must be packaged on the
# given day. Date, delivery address and weekday are the most important factors in determining the day that the orderline
# will be assigned to. The logic respects the current rules laid out by Hay and DSV.
#
# Finally, orderlines with the same delivery address on a given day are grouped together and a Kid object is
# instantiated. A Kid will, for practical purposes, present itself as an order and will appear as such for the
# packers at the warehouse.


def main():
    app = QApplication([])
    app.setStyleSheet(stylesheet.stylesheet)
    window = MainWindow()
    window.setWindowIcon(QIcon("report-icon.ico"))
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
