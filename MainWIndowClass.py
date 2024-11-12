from pathlib import Path
from PyQt6.QtWidgets import (QMainWindow,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QLineEdit,
                             QPushButton,
                             QFileDialog,
                             QCheckBox,
                             QSpacerItem)
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt

from DataProcessing import ReportGeneratorThread
from popup_messagebox import show_popup


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Palissade Ugerapportgenerator")
        self.setFixedSize(400, 140)
        screen = QGuiApplication.primaryScreen().geometry()
        center_pos_x = (screen.width() - self.width()) // 2
        center_pos_y = (screen.height() - self.height()) // 2
        self.move(center_pos_x, center_pos_y)
        self.keep_sql_file: bool = False

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(16, 16, 16, 16)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        output_layout = QHBoxLayout()
        output_layout.setSpacing(10)

        self.input_path_line_edit = QLineEdit()
        self.input_path_line_edit.setPlaceholderText("Input (.xlsx)")
        self.input_path_line_edit.setFixedHeight(24)

        self.browse_input_path_button = QPushButton("Gennemse")
        self.browse_input_path_button.setFixedWidth(80)
        self.browse_input_path_button.setFixedHeight(24)
        self.browse_input_path_button.clicked.connect(self.browse_input_file)

        self.output_path_line_edit = QLineEdit()
        self.output_path_line_edit.setPlaceholderText("Output (.html)")
        self.output_path_line_edit.setFixedHeight(24)

        self.browse_output_path_button = QPushButton("Gennemse")
        self.browse_output_path_button.setFixedWidth(80)
        self.browse_output_path_button.setFixedHeight(24)
        self.browse_output_path_button.clicked.connect(self.browse_output_file)

        self.spacer = QSpacerItem(0, 3)

        self.sql_checkbox = QCheckBox("Behold SQL-filen")
        self.sql_checkbox.stateChanged.connect(self.sql_checkbox_changed)

        self.start_button = QPushButton("Start")
        self.start_button.setFixedWidth(80)
        self.start_button.setFixedHeight(24)

        self.start_button.clicked.connect(self.generate_report)

        input_layout.addWidget(self.input_path_line_edit)
        input_layout.addWidget(self.browse_input_path_button, alignment=Qt.AlignmentFlag.AlignLeft)
        output_layout.addWidget(self.output_path_line_edit)
        output_layout.addWidget(self.browse_output_path_button, alignment=Qt.AlignmentFlag.AlignLeft)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addItem(self.spacer)
        main_layout.addWidget(self.sql_checkbox, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        central_widget.setLayout(main_layout)

    def browse_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Vælg input fil", "",
                                                   "Excel Filer (*.xlsx);;Alle Filer (*)")
        if file_name:
            self.input_path_line_edit.setText(file_name)

    def browse_output_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Vælg output fil", "Ugerapport.html",
                                                   "HTML Filer (*.html);;Alle Filer (*)")
        if file_name:
            self.output_path_line_edit.setText(file_name)

    def sql_checkbox_changed(self, state):
        if state == 2:
            self.keep_sql_file = True
        else:
            self.keep_sql_file = False

    def generate_report(self):
        input_path = Path(self.input_path_line_edit.text())
        output_path = Path(self.output_path_line_edit.text())
        if input_path and output_path:
            self.thread = ReportGeneratorThread(input_path, output_path, self.keep_sql_file)
            self.thread.finished.connect(self.show_finished_popup)
            self.thread.start()

    @staticmethod
    def show_finished_popup():
        show_popup("Færdig", "Rapporten er dannet.", "information")
