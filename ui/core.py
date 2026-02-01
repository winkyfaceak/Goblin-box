from PyQt6.QtWidgets import (
    QMainWindow, QStackedWidget
)

from .dictation import DictationWindow
from .home import HomePage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("goblin box")
        self.setGeometry(100, 100, 600, 500)

        # Use QStackedWidget instead of replacing central widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create pages
        self.home_page = HomePage()
        self.dictation_page = DictationWindow()

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.home_page)  # Index 0
        self.stacked_widget.addWidget(self.dictation_page)  # Index 1

        # Create a mapping of page names to indices
        self.page_indices = {
            "home": 0,
            "dictation": 1
        }

        # Connect signals from both pages
        self.home_page.switch_page.connect(self.switch_to_page)
        self.dictation_page.switch_page.connect(self.switch_to_page)

        # Start on home page
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_page(self, page_name):
        """Switch to a page by name"""
        if page_name in self.page_indices:
            index = self.page_indices[page_name]
            self.stacked_widget.setCurrentIndex(index)
