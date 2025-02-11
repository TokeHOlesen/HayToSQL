from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
import os
import sys


def display_popup(title: str, message: str, icon: str) -> None:
    """Spawns a MessageBox with a given title, content and icon."""
    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(message)
    icon_file = "report_icon.ico"
    icon_path = os.path.join(sys._MEIPASS, icon_file) if hasattr(sys, "_MEIPASS") else icon_file
    message_box.setWindowIcon(QIcon(icon_path))
    ok_button = message_box.addButton(QMessageBox.StandardButton.Ok)
    ok_button.setFixedSize(QSize(80, 20))
    match icon:
        case "warning":
            message_box.setIcon(QMessageBox.Icon.Warning)
        case "information":
            message_box.setIcon(QMessageBox.Icon.Information)
        case "critical":
            message_box.setIcon(QMessageBox.Icon.Critical)
        case _:
            message_box.setIcon(QMessageBox.Icon.NoIcon)
    message_box.exec()
