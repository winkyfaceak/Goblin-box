from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class HomePage(QWidget):
    switch_page = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        title = QLabel("Home")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_dictation = QPushButton("Go to Dictation")

        btn_dictation.clicked.connect(lambda: self.switch_page.emit("dictation"))

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(btn_dictation)
        layout.addStretch()

        self.setLayout(layout)