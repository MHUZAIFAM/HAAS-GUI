from PyQt5.QtWidgets import QApplication, QStackedWidget, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
from intro_page import IntroPage
from profile_page import ProfilePage
from tutorial_page import TutorialPage

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Frailty Assessment Project")
        self.resize(1920, 1080)

        # Stack for switching pazzzges
        self.stacked_widget = QStackedWidget()

        # Create pages and pass self as parent
        self.intro_page = IntroPage(self)
        self.profile_page = ProfilePage(self)
        self.tutorial_page = TutorialPage(self)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.intro_page)
        self.stacked_widget.addWidget(self.profile_page)
        self.stacked_widget.addWidget(self.tutorial_page)

        # Layout for the main window
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # Start with Intro Page
        self.stacked_widget.setCurrentWidget(self.intro_page)

        # Automatically transition from intro to profile page
        QTimer.singleShot(3000, self.show_profile_page)

    def setCurrentWidget(self, widget):
        """Helper function to switch pages"""
        self.stacked_widget.setCurrentWidget(widget)

    def show_profile_page(self):
        """Switch to the Profile Page"""
        self.setCurrentWidget(self.profile_page)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
