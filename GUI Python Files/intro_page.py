# intro_page.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class IntroPage(QWidget):
    def __init__(self, parent=None):  # Add parent argument
        super().__init__(parent)  # Pass parent to QWidget
        self.setWindowTitle("Introduction Page")
        self.resize(1920, 1080)

        # Layout for intro page
        layout = QVBoxLayout()
        label = QLabel("PROJECT HAAS")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 100, QFont.Bold))
        label.setStyleSheet("color: black;")

        layout.addWidget(label)
        self.setLayout(layout)
