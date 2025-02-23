import csv
import os
import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
import subprocess
import sys

class TutorialPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tutorial Page")
        self.resize(800, 600)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Select a Test")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

        # Ordered list of test names and corresponding executables
        self.test_executables = {
            "Walking Speed Test": "Walking_Speed.exe",
            "Functional Reach Test": "Functional_Reach.exe",
            "Timed Up and Go (TUG)": "TUG_Test.exe",
            "Standing on One Leg with Eye Open Test": "One_Leg_Standing.exe",
            "Seated Forward Bend Test": "Seated_Forward.exe",
        }

        self.patient_data_file = "Patient_Data.csv"
        self.repeat_test = False  # Flag to track if test is repeated
        self.current_patient_id = "1234"  # Placeholder, should be set dynamically

        # Creating test buttons
        for test, exe_file in self.test_executables.items():
            test_layout = QHBoxLayout()

            test_label = QLabel(test)
            test_label.setFixedWidth(300)
            test_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            test_layout.addWidget(test_label)

            demo_button = QPushButton("Demo Video")
            demo_button.setFixedHeight(50)
            demo_button.setStyleSheet("font-size: 16px; padding: 12px;")
            demo_button.clicked.connect(lambda _, t=test: self.show_demo(t))
            test_layout.addWidget(demo_button)

            start_button = QPushButton("Start Test")
            start_button.setFixedHeight(50)
            start_button.setStyleSheet("font-size: 16px; padding: 12px; background-color: #4CAF50; color: white; border-radius: 6px;")
            start_button.clicked.connect(lambda _, e=exe_file, t=test: self.start_test(e, t))
            test_layout.addWidget(start_button)

            repeat_button = QPushButton("Repeat Test")
            repeat_button.setFixedHeight(50)
            repeat_button.setStyleSheet("font-size: 16px; padding: 12px; background-color: #FF9800; color: white; border-radius: 6px;")
            repeat_button.clicked.connect(lambda _, e=exe_file, t=test: self.repeat_test_function(e, t))
            test_layout.addWidget(repeat_button)

            main_layout.addLayout(test_layout)

        # Back, Combine Data, Generate Results, and Send Data buttons layout
        button_layout = QHBoxLayout()

        back_button = QPushButton("Back")
        back_button.setFixedHeight(50)
        back_button.setStyleSheet("font-size: 16px; padding: 12px; background-color: #005f87; color: white; border-radius: 8px;")
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        combine_button = QPushButton("Combine Data")
        combine_button.setFixedHeight(50)
        combine_button.setStyleSheet("font-size: 16px; padding: 12px; background-color: #673AB7; color: white; border-radius: 8px;")
        combine_button.clicked.connect(self.combine_data)
        button_layout.addWidget(combine_button)

        generate_results_button = QPushButton("Generate Results")
        generate_results_button.setFixedHeight(50)
        generate_results_button.setStyleSheet("font-size: 16px; padding: 12px; background-color: #FF5722; color: white; border-radius: 8px;")
        generate_results_button.clicked.connect(self.generate_results)
        button_layout.addWidget(generate_results_button)

        send_button = QPushButton("Send Data")
        send_button.setFixedHeight(50)
        send_button.setStyleSheet("font-size: 16px; padding: 12px; background-color: #2196F3; color: white; border-radius: 8px;")
        send_button.clicked.connect(self.send_data_to_server)
        button_layout.addWidget(send_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def show_demo(self, test_name):
        """Play demo video only for Functional Reach Test."""
        if test_name == "Functional Reach Test":
            video_file = "Functional Reach Test Animated Demo.mp4"
            if os.path.exists(video_file):
                if sys.platform == "win32":
                    os.startfile(video_file)
                elif sys.platform == "darwin":
                    subprocess.run(["open", video_file])
                else:
                    subprocess.run(["xdg-open", video_file])
            else:
                print(f"Video file '{video_file}' not found.")
        else:
            print(f"No demo available for {test_name}")

    def send_data_to_server(self):
        """Reads patient data from CSV and sends it to the server."""
        if not os.path.exists(self.patient_data_file):
            print("Patient data file not found.")
            return

        try:
            with open(self.patient_data_file, "r", newline="") as file:
                reader = csv.DictReader(file)
                data_list = [row for row in reader]

            if not data_list:
                print("No data found in the CSV file.")
                return

            response = requests.post("http://localhost:3000/send-data", json=data_list)

            if response.status_code == 200:
                print("Data sent successfully!")
            else:
                print(f"Error sending data: {response.text}")

        except Exception as e:
            print(f"Failed to send data: {e}")

    def start_test(self, exe_file, test_name):
        self.repeat_test = False
        test_result = self.run_test(exe_file)
        if test_result is not None:
            self.save_test_result(test_name, test_result)

    def repeat_test_function(self, exe_file, test_name):
        self.repeat_test = True
        test_result = self.run_test(exe_file)
        if test_result is not None:
            self.save_test_result(test_name, test_result)

    def run_test(self, exe_file):
        try:
            result = subprocess.run([exe_file], check=True, capture_output=True, text=True)
            output = result.stdout.strip()
            print(f"CLI Output: {output}")
            elapsed_time = float(output.split(":")[-1].strip().replace("s", ""))
            return elapsed_time
        except Exception as e:
            print(f"Error running {exe_file}: {e}")
            return None

    def save_test_result(self, test_name, test_value):
        print(f"Saving {test_name} result: {test_value}")

    def combine_data(self):
        try:
            subprocess.run(["python", "Data Combination.py"], check=True)
        except Exception as e:
            print(f"Error combining data: {e}")

    def generate_results(self):
        try:
            subprocess.run(["python", "Generate Results.py"], check=True)
        except Exception as e:
            print(f"Error generating results: {e}")

    def go_back(self):
        self.parent().setCurrentIndex(0)
