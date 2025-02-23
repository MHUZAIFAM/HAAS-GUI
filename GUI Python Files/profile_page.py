from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import os


class ProfilePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Profile Page")
        self.resize(1000, 800)

        layout = QVBoxLayout()

        # Profile image setup
        image_label = QLabel()
        pixmap = QPixmap("Resources/Profile Page.png")
        image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        # Function to create input bars for ID, age, and gender
        def create_input_field(label_text):
            field_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 16px; font-weight: bold;")
            input_field = QLineEdit()
            input_field.setFixedHeight(40)
            input_field.setMinimumWidth(500)
            field_layout.addWidget(label)
            field_layout.addWidget(input_field)
            return field_layout, input_field

        # Create input fields
        id_layout, self.id_input = create_input_field("ID:  ")
        layout.addLayout(id_layout)
        age_layout, self.age_input = create_input_field("Age: ")
        layout.addLayout(age_layout)
        gender_layout, self.gender_input = create_input_field("Gender: ")
        layout.addLayout(gender_layout)

        # Save button
        save_button = QPushButton("Save")
        save_button.setFixedHeight(40)
        save_button.setFixedWidth(120)
        save_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px;")
        save_button.clicked.connect(self.save_profile_data)
        layout.addWidget(save_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def save_profile_data(self):
        """Save profile data with validation"""
        user_id = self.id_input.text().strip()
        age = self.age_input.text().strip()
        gender = self.gender_input.text().strip().capitalize()

        # Validation
        if not user_id.isdigit():
            QMessageBox.warning(self, "Input Error", "ID must be a whole number.")
            return

        if not age.isdigit():
            QMessageBox.warning(self, "Input Error", "Age must be a whole number.")
            return

        if gender not in ["Male", "Female"]:
            QMessageBox.warning(self, "Input Error", "Gender must be either 'Male' or 'Female'.")
            return

        file_path = "Patient_Data.csv"
        file_exists = os.path.isfile(file_path)

        with open(file_path, "a") as file:
            if not file_exists:
                file.write("ID,Age,Gender\n")
            file.write(f"{user_id},{age},{gender}\n")

        self.parent.setCurrentWidget(self.parent.tutorial_page)
