from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon


def display_popup(title: str, message: str, icon: str) -> None:
    """Spawns a MessageBox with the given title and content."""
    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setWindowIcon(QIcon("report-icon.ico"))
    ok_button = message_box.addButton(QMessageBox.StandardButton.Ok)
    ok_button.setFixedSize(QSize(80, 20))
    match icon:
        case "warning":
            message_box.setIcon(QMessageBox.Icon.Warning)
        case "information":
            message_box.setIcon(QMessageBox.Icon.Information)
        case _:
            message_box.setIcon(QMessageBox.Icon.NoIcon)
    message_box.exec()
