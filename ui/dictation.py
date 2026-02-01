from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout  # Changed from QMainWindow


class DictationWindow(QWidget):  # Changed to QWidget - it's a page, not a window
    switch_page = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        dictation_button = QPushButton("start dictation")
        back_btn = QPushButton("← Back to Home")
        back_btn.clicked.connect(lambda: self.switch_page.emit("home"))
        layout.addStretch()
        layout.addWidget(back_btn)
        layout.addWidget(dictation_button)

        self.setLayout(layout)
