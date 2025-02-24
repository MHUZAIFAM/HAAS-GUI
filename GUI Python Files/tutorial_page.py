import csv
import os
import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
import subprocess
import sys
import shutil


class TutorialPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tutorial Page")
        self.resize(800, 600)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header Layout (for Logos)
        header_layout = QHBoxLayout()

        # Load NUST logo (Top-Left)
        nust_logo = QLabel()
        nust_pixmap = QPixmap(os.path.join(os.getcwd(), "Resources", "NUST.png"))
        nust_logo.setPixmap(nust_pixmap.scaled(200,200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header_layout.addWidget(nust_logo, alignment=Qt.AlignLeft | Qt.AlignTop)

        # **PROJECT HAAS Title in the Center**
        title_label = QLabel("PROJECT HAAS")
        title_label.setFont(QFont("Arial", 50, QFont.Bold))  # Set font size and bold
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #333;")  # Optional: Text color
        header_layout.addWidget(title_label, alignment=Qt.AlignCenter)



        # Load JUNTENDO logo (Top-Right)
        juntendo_logo = QLabel()
        juntendo_pixmap = QPixmap(os.path.join(os.getcwd(), "Resources", "JUNTENDO.png"))
        juntendo_logo.setPixmap(juntendo_pixmap.scaled(200,200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header_layout.addWidget(juntendo_logo, alignment=Qt.AlignRight | Qt.AlignTop)

        # Add Header to Main Layout
        main_layout.addLayout(header_layout)


        # Ordered list of test names and corresponding executables
        self.test_executables = {
            "Walking Speed": ("Walking_Speed_1.exe", "Walking_Speed_2.exe"),
            "Functional Reach": ("Functional_Reach_1.exe", "Functional_Reach_2.exe"),
            "Timed Up and Go": ("TUG_Test_1.exe", "TUG_Test_2.exe"),
            "Standing on One Leg with Eye Open": ("One_Leg_Standing_1.exe", "One_Leg_Standing_2.exe"),
            "Seated Forward Bend": ("Seated_Forward_1.exe", "Seated_Forward_2.exe"),
        }

        self.patient_data_file = "Patient_Data.csv"
        self.repeat_test = False  # Flag to track if test is repeated
        self.current_patient_id = "1234"  # Placeholder, should be set dynamically

        # Creating test buttons
        # Creating test buttons
        for test, (exe_start, exe_repeat) in self.test_executables.items():
            test_layout = QHBoxLayout()

            test_label = QLabel(test)
            test_label.setFixedWidth(300)
            test_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            test_layout.addWidget(test_label)

            demo_button = QPushButton("Demo Video")
            demo_button.setFixedHeight(50)
            demo_button.setStyleSheet("""
                QPushButton {
                    font-size: 16px; 
                    padding: 12px; 
                    background-color: #e0e0e0; 
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #d6d6d6;
                }
                QPushButton:pressed {
                    background-color: #bdbdbd;
                    padding: 14px 12px;
                }
            """)
            demo_button.clicked.connect(lambda _, t=test: self.show_demo(t))
            test_layout.addWidget(demo_button)

            start_button = QPushButton("Start Test")
            start_button.setFixedHeight(50)
            start_button.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    padding: 12px;
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 6px;
                    transition: all 0.2s ease-in-out;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #388E3C;
                    padding: 14px 12px;
                }
            """)
            start_button.clicked.connect(lambda _, e=exe_start, t=test: self.start_test(e, t))
            test_layout.addWidget(start_button)

            repeat_button = QPushButton("Repeat Test")
            repeat_button.setFixedHeight(50)
            repeat_button.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    padding: 12px;
                    background-color: #FF9800;
                    color: white;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #e68900;
                }
                QPushButton:pressed {
                    background-color: #d17a00;
                    padding: 14px 12px;
                }
            """)
            repeat_button.clicked.connect(lambda _, e=exe_repeat, t=test: self.repeat_test_function(e, t))
            test_layout.addWidget(repeat_button)

            skip_button = QPushButton("Skip Test")
            skip_button.setFixedHeight(50)
            skip_button.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    padding: 12px;
                    background-color: #F44336;
                    color: white;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
                QPushButton:pressed {
                    background-color: #b71c1c;
                    padding: 14px 12px;
                }
            """)
            skip_button.clicked.connect(lambda _, t=test: self.skip_test(t))
            test_layout.addWidget(skip_button)

            main_layout.addLayout(test_layout)

        # Back, Combine Data, Generate Results, and Send Data buttons layout
        button_layout = QHBoxLayout()

        back_button = QPushButton("Back")
        back_button.setFixedHeight(50)
        back_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 12px;
                background-color: #005f87;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #004a6d;
            }
            QPushButton:pressed {
                background-color: #003752;
                padding: 14px 12px;
            }
        """)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        combine_button = QPushButton("Combine Data")
        combine_button.setFixedHeight(50)
        combine_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 12px;
                background-color: #673AB7;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5a2ea3;
            }
            QPushButton:pressed {
                background-color: #482480;
                padding: 14px 12px;
            }
        """)
        combine_button.clicked.connect(self.combine_data)
        button_layout.addWidget(combine_button)

        generate_results_button = QPushButton("Generate Results")
        generate_results_button.setFixedHeight(50)
        generate_results_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 12px;
                background-color: #FF5722;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #e64a19;
            }
            QPushButton:pressed {
                background-color: #d84315;
                padding: 14px 12px;
            }
        """)
        generate_results_button.clicked.connect(self.generate_results)
        button_layout.addWidget(generate_results_button)

        send_button = QPushButton("Send Data")
        send_button.setFixedHeight(50)
        send_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 12px;
                background-color: #2196F3;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1e88e5;
            }
            QPushButton:pressed {
                background-color: #1565c0;
                padding: 14px 12px;
            }
        """)
        send_button.clicked.connect(self.send_data_to_server)
        button_layout.addWidget(send_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    import os
    import sys
    import subprocess

    import os
    import sys
    import subprocess

    def show_demo(self, test_name):
        """Play the corresponding demo video for the selected test using VLC."""

        demo_videos = {
            "Walking Speed Test": "Walking_Speed_Demo.mp4",
            "Functional Reach Test": "Functional_Reach_Test_Animated_Demo.mp4",
            "Timed Up and Go (TUG)": "TUG_Demo.mp4",
            "Standing on One Leg with Eye Open Test": "One_Leg_Standing_Demo.mp4",
            "Seated Forward Bend Test": "Seated_Forward_Bend_Demo.mp4"
        }

        # Find best matching key if an exact match isn't found
        video_file = demo_videos.get(test_name)
        if not video_file:
            for key in demo_videos:
                if test_name.lower() in key.lower():  # Case-insensitive partial match
                    video_file = demo_videos[key]
                    break

        if video_file:
            abs_path = os.path.abspath(video_file)
            print(f"Attempting to open: {abs_path}")  # Debugging print

            if os.path.exists(abs_path):
                vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
                if os.path.exists(vlc_path):
                    subprocess.run([vlc_path, abs_path])  # Open with VLC
                else:
                    print("VLC not found. Trying system default player...")
                    if sys.platform == "win32":
                        os.startfile(abs_path)
                    elif sys.platform == "darwin":
                        subprocess.run(["open", abs_path])
                    else:
                        subprocess.run(["xdg-open", abs_path])
            else:
                print(f"Error: Video file '{abs_path}' not found.")
        else:
            print(f"Error: No demo video mapped for '{test_name}'")


    def send_data_to_server(self):
        """Copies data.csv to the target directory."""

        # Define source and destination paths
        source_file = "data.csv"  # Assuming it's in the same directory as the script
        destination_dir = r"C:\Users\mhuza\source\repos\Project HaaS\Project HaaS"
        destination_file = os.path.join(destination_dir, "data.csv")

        # Check if source file exists
        if not os.path.exists(source_file):
            print("Source data file not found.")
            return

        try:
            # Copy the file
            shutil.copy(source_file, destination_file)
            print(f"Data successfully copied to: {destination_file}")
        except Exception as e:
            print(f"Failed to copy data: {e}")

    def start_test(self, exe_file, test_name):
        """Starts the first test execution."""
        try:
            subprocess.Popen(exe_file)
            print(f"Started test: {test_name} ({exe_file})")
        except FileNotFoundError:
            print(f"Error: {exe_file} not found!")

    def repeat_test_function(self, exe_file, test_name):
        """Repeats the test execution."""
        try:
            subprocess.Popen(exe_file)
            print(f"Repeated test: {test_name} ({exe_file})")
        except FileNotFoundError:
            print(f"Error: {exe_file} not found!")
    import csv

    import csv
    import os

    import csv
    import os

    def skip_test(self, test_name):
        """Creates a CSV file with a single NULL entry if the test is skipped.
           If the file already exists, it does nothing (ensures only one NULL row)."""

        # Mapping test names to corresponding CSV filenames and headers
        test_csv_mapping = {
            "Walking Speed Test": ("Walking_Speed_Test_Results_2.csv", ["Walking Speed Test (s) 2"]),
            "Functional Reach Test": ("Functional_Reach_Test_Results_2.csv", ["Functional Reach Test (cm) 2"]),
            "Timed Up and Go (TUG)": ("Time_Up_and_Go_Test_Results_2.csv", ["Time Up and Go Test (s) 2"]),
            "Standing on One Leg with Eye Open Test": (
            "Standing_on_One_Leg_with_Eye_Open_Test_Results_2.csv", ["Standing on One Leg with Eye Open Test (s) 2"]),
            "Seated Forward Bend Test": ("Seated_Forward_Bend_Test_Results_2.csv", ["Seated Forward Bend Test (s) 2"])
        }

        if test_name in test_csv_mapping:
            csv_filename, header = test_csv_mapping[test_name]

            # Check if the file already exists
            if os.path.exists(csv_filename):
                print(f"{test_name} already skipped. No changes made to '{csv_filename}'.")
                return  # Exit function to prevent duplicate entries

            try:
                with open(csv_filename, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(header)  # Write the header
                    writer.writerow(["NULL"])  # Write only one NULL row

                print(f"{test_name} skipped. CSV file '{csv_filename}' created with a single entry.")

            except Exception as e:
                print(f"Error creating {csv_filename}: {e}")

        else:
            print(f"Unknown test: {test_name}")

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
        previous_index = self.parent().property("previous_index")  # Retrieve stored index
        if previous_index is not None:
            self.parent().setCurrentIndex(previous_index)  # Go back to last page
        else:
            self.parent().setCurrentIndex(0)  # Default to home if no previous index is found

