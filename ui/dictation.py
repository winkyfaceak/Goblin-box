from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout  # Changed from QMainWindow


class DictationWindow(QWidget):  # Changed to QWidget - it's a page, not a window
    switch_page = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        title = QLabel("Dictation Page")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        back_btn = QPushButton("← Back to Home")
        back_btn.clicked.connect(lambda: self.switch_page.emit("home"))

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)