from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from PyQt5.QtCore import Qt


class ProfilePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Profile Page")
        self.resize(1000, 800)
        self.setStyleSheet("background-color: #F5F7FA;")  # Soft light gray background

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 80, 50, 50)  # Adjust margins

        # Profile Image
        image_label = QLabel()
        pixmap = QPixmap("Resources/Profile Page.png")
        image_label.setPixmap(pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        # Function to create input fields
        def create_input_field(label_text, placeholder):
            field_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFont(QFont("Montserrat", 14, QFont.Bold))
            label.setStyleSheet("color: #333; padding: 8px;")

            input_field = QLineEdit()
            input_field.setFixedHeight(50)
            input_field.setMinimumWidth(400)
            input_field.setAlignment(Qt.AlignCenter)
            input_field.setPlaceholderText(placeholder)  # Set placeholder
            input_field.setStyleSheet("""
                QLineEdit {
                    font-size: 16px;
                    padding: 8px;
                    border: 2px solid #CCC;
                    border-radius: 10px;
                    background-color: white;
                }
                QLineEdit:focus {
                    border: 2px solid #1E90FF;
                    background-color: #E6F7FF;
                }
            """)

            field_layout.addWidget(label)
            field_layout.addWidget(input_field)
            return field_layout, input_field

        # Create input fields
        id_layout, self.id_input = create_input_field("ID:", "Enter ID (Numbers only)")
        layout.addLayout(id_layout)

        age_layout, self.age_input = create_input_field("Age:", "Enter Age")
        layout.addLayout(age_layout)

        gender_layout, self.gender_input = create_input_field("Gender:", "Male / Female")
        layout.addLayout(gender_layout)

        # Divider Line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("background-color: #AAA; margin: 20px;")
        layout.addWidget(divider)

        # Save Button
        save_button = QPushButton("Save Profile")
        save_button.setFixedHeight(50)
        save_button.setFixedWidth(200)
        save_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                color: white;
                border-radius: 10px;
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #4CAF50, stop:1 #2E7D32);
                padding: 10px;
            }
            QPushButton:hover {
                background: #388E3C;
            }
            QPushButton:pressed {
                background: #1B5E20;
            }
        """)
        save_button.clicked.connect(self.save_profile_data)
        layout.addWidget(save_button, alignment=Qt.AlignHCenter)

        self.setLayout(layout)

    def save_profile_data(self):
        """Save profile data with validation and overwrite previous entry"""
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

        # Overwrite file with latest entry
        with open(file_path, "w") as file:
            file.write("Recipient ID,Age,Gender\n")  # Write header
            file.write(f"{user_id},{age},{gender}\n")  # Save latest entry only

        self.parent.setCurrentWidget(self.parent.tutorial_page)
