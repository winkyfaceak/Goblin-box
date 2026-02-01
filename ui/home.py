from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class HomePage(QWidget):
    """Home page with navigation to dictation and transcription"""
    switch_page = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Goblin Box")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtitle
        subtitle = QLabel("Choose a mode:")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Dictation button
        btn_dictation = QPushButton("🎤 Live Dictation")
        btn_dictation.setStyleSheet("font-size: 16px; padding: 15px;")
        btn_dictation.clicked.connect(lambda: self.switch_page.emit("dictation"))

        # Transcription button
        btn_transcription = QPushButton("📁 Transcribe Audio File")
        btn_transcription.setStyleSheet("font-size: 16px; padding: 15px;")
        btn_transcription.clicked.connect(lambda: self.switch_page.emit("transcription"))

        # Layout
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(30)
        layout.addWidget(btn_dictation)
        layout.addWidget(btn_transcription)
        layout.addStretch()

        self.setLayout(layout)