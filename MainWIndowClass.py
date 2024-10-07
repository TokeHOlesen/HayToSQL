from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Palissade Ugerapport Generator")
        self.setFixedSize(400, 134)
        screen = QGuiApplication.primaryScreen().geometry()
        center_pos_x = (screen.width() - self.width()) // 2
        center_pos_y = (screen.height() - self.height()) // 2
        self.move(center_pos_x, center_pos_y)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(16, 16, 16, 16)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        output_layout = QHBoxLayout()
        output_layout.setSpacing(10)

        self.input_path_line_edit = QLineEdit()
        self.input_path_line_edit.setPlaceholderText("Input fil (.xlsx)")

        self.browse_input_path_button = QPushButton("Gennemse")
        self.browse_input_path_button.setFixedWidth(80)

        self.output_path_line_edit = QLineEdit()
        self.output_path_line_edit.setPlaceholderText("Output fil (.html)")

        self.browse_output_path_button = QPushButton("Gennemse")
        self.browse_output_path_button.setFixedWidth(80)

        self.start_button = QPushButton("Start")
        self.start_button.setFixedWidth(60)

        input_layout.addWidget(self.input_path_line_edit)
        input_layout.addWidget(self.browse_input_path_button, alignment=Qt.AlignmentFlag.AlignLeft)
        output_layout.addWidget(self.output_path_line_edit)
        output_layout.addWidget(self.browse_output_path_button, alignment=Qt.AlignmentFlag.AlignLeft)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        central_widget.setLayout(main_layout)
