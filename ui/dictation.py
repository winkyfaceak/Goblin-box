from PyQt6.QtCore import pyqtSignal, QThread
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout, QLabel

from audio import recorder
from stt import whisper_engine


class DictationThread(QThread):
    """Background thread for live dictation"""
    text_transcribed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.is_running = True
        self.is_paused = False
        self.recorder = recorder.AudioRecorder()
        self.whisper = whisper_engine.WhisperEngine(model_size="base")

    def run(self):
        while self.is_running:
            if not self.is_paused:
                try:
                    audio = self.recorder.record(duration=5)
                    text = self.whisper.transcribe(audio_np=audio)
                    if text:
                        self.text_transcribed.emit(text)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                self.msleep(100)

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def stop(self):
        self.is_running = False
        self.wait()


class DictationPage(QWidget):
    """Live dictation page - records and transcribes in real-time"""
    switch_page = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Live Dictation")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Status
        self.status_label = QLabel("Ready to record")

        # Text display
        self.text_display = QTextEdit()
        self.text_display.setPlaceholderText("Start dictation and speak...")
        self.text_display.setMinimumHeight(350)

        # Control buttons
        control_layout = QHBoxLayout()

        self.start_btn = QPushButton("Start Dictation")
        self.start_btn.clicked.connect(self.start_dictation)

        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.pause_btn.setEnabled(False)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_dictation)
        self.stop_btn.setEnabled(False)

        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.stop_btn)

        # Utility buttons
        utility_layout = QHBoxLayout()

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.text_display.clear)

        utility_layout.addWidget(clear_btn)

        # Back button
        back_btn = QPushButton("← Back to Home")
        back_btn.clicked.connect(lambda: self.switch_page.emit("home"))

        # Layout
        layout.addWidget(title)
        layout.addWidget(self.status_label)
        layout.addLayout(control_layout)
        layout.addWidget(self.text_display)
        layout.addLayout(utility_layout)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

        self.dictation_thread = None
        self.is_paused = False

    def start_dictation(self):
        """Start live dictation"""
        if self.dictation_thread is None or not self.dictation_thread.isRunning():
            self.dictation_thread = DictationThread()
            self.dictation_thread.text_transcribed.connect(self.append_text)
            self.dictation_thread.start()

            self.start_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.stop_btn.setEnabled(True)
            self.status_label.setText("🔴 Recording...")
            self.is_paused = False

    def toggle_pause(self):
        """Pause/resume dictation"""
        if self.dictation_thread and self.dictation_thread.isRunning():
            if self.is_paused:
                self.dictation_thread.resume()
                self.pause_btn.setText("Pause")
                self.status_label.setText("🔴 Recording...")
                self.is_paused = False
            else:
                self.dictation_thread.pause()
                self.pause_btn.setText("Resume")
                self.status_label.setText("⏸ Paused")
                self.is_paused = True

    def stop_dictation(self):
        """Stop dictation"""
        if self.dictation_thread:
            self.dictation_thread.stop()
            self.dictation_thread = None

            self.start_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)
            self.pause_btn.setText("Pause")
            self.status_label.setText("Stopped")
            self.is_paused = False

    def append_text(self, text):
        """Add transcribed text"""
        cursor = self.text_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.text_display.setTextCursor(cursor)
        self.text_display.insertPlainText(text + " ")