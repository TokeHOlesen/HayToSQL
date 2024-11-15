# Used to style the main window.

stylesheet = """
        QLineEdit {
            border: 1px solid #AAAAAA;
            border-radius: 4px;
            padding: 2px;
            background: white;
        }
        QPushButton {
            background-color: #F4F4F4;
            border: 1px solid #AAAAAA;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #FFFFFF;
        }
        QPushButton:focus {
            border: 2px solid #AAAAAA;
        }
        QPushButton:disabled {
            color: #BBBBBB;
        }
        QLabel#label_preview {
            border: 2px solid #AAAAAA;
            color: #CCCCCC;
        }
"""