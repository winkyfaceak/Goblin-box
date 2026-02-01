import sys
from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from ui import TranscriptionPage, HomePage
from ui.dictation import DictationPage


class MainWindow(QMainWindow):
    """Main window with navigation between pages"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Goblin Box")
        self.setGeometry(100, 100, 700, 600)

        # Crates widget stack
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Creates all pages
        self.home_page = HomePage()
        self.dictation_page = DictationPage()
        self.transcription_page = TranscriptionPage()

        # Add pages to stack
        self.stacked_widget.addWidget(self.home_page)  # Index 0
        self.stacked_widget.addWidget(self.dictation_page)  # Index 1
        self.stacked_widget.addWidget(self.transcription_page)  # Index 2

        # Page name to index mapping
        self.page_indices = {
            "home": 0,
            "dictation": 1,
            "transcription": 2
        }

        # Connect all page signals
        self.home_page.switch_page.connect(self.switch_to_page)
        self.dictation_page.switch_page.connect(self.switch_to_page)
        self.transcription_page.switch_page.connect(self.switch_to_page)

        # Start on home page
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_page(self, page_name):
        """Navigate to a page by name"""
        if page_name in self.page_indices:
            index = self.page_indices[page_name]
            self.stacked_widget.setCurrentIndex(index)