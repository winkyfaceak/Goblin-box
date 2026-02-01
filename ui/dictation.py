from PyQt6.QtCore import pyqtSignal, QThread
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout

from audio import recorder
from stt import whisper_engine


class DictationThread(QThread):
    """Separate thread for dictation so UI doesn't freeze"""
    text_transcribed = pyqtSignal(str)  # Signal to send transcribed text

    def __init__(self):
        super().__init__()
        self.is_running = True
        self.is_paused = False
        self.recorder = recorder.AudioRecorder()
        self.whisper = whisper_engine.WhisperEngine(model_size="base")

    def run(self):
        """This runs in the background thread"""
        while self.is_running:
            if not self.is_paused:
                try:
                    audio = self.recorder.record(duration=5)
                    text = self.whisper.transcribe(audio_np=audio)
                    if text:
                        self.text_transcribed.emit(text)  # Send text to UI
                except Exception as e:
                    print(f"Error: {e}")
            else:
                # Sleep a bit when paused to not waste CPU
                self.msleep(100)

    def pause(self):
        """Pause dictation"""
        self.is_paused = True

    def resume(self):
        """Resume dictation"""
        self.is_paused = False

    def stop(self):
        """Stop the thread"""
        self.is_running = False
        self.wait()  # Wait for thread to finish


class DictationWindow(QWidget):
    switch_page = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Text display area
        self.text_display = QTextEdit()
        self.text_display.setPlaceholderText("Transcribed text will appear here...")
        self.text_display.setMinimumHeight(300)

        # Control buttons in a horizontal layout
        button_layout = QHBoxLayout()

        self.start_btn = QPushButton("Start Dictation")
        self.start_btn.clicked.connect(self.start_dictation)

        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.pause_btn.setEnabled(False)  # Disabled until dictation starts

        self.stop_btn = QPushButton("Stop Dictation")
        self.stop_btn.clicked.connect(self.stop_dictation)
        self.stop_btn.setEnabled(False)  # Disabled until dictation starts

        clear_btn = QPushButton("Clear Text")
        clear_btn.clicked.connect(self.clear_text)

        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(clear_btn)

        # Back button
        back_btn = QPushButton("← Back to Home")
        back_btn.clicked.connect(lambda: self.switch_page.emit("home"))

        # Add everything to layout
        layout.addWidget(self.text_display)
        layout.addLayout(button_layout)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

        # Dictation thread (not started yet)
        self.dictation_thread = None
        self.is_paused = False

    def start_dictation(self):
        """Start the dictation thread"""
        if self.dictation_thread is None or not self.dictation_thread.isRunning():
            self.dictation_thread = DictationThread()
            self.dictation_thread.text_transcribed.connect(self.append_text)
            self.dictation_thread.start()

            # Update button states
            self.start_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.stop_btn.setEnabled(True)
            self.pause_btn.setText("Pause")
            self.is_paused = False

    def toggle_pause(self):
        """Pause or resume dictation"""
        if self.dictation_thread and self.dictation_thread.isRunning():
            if self.is_paused:
                # Resume
                self.dictation_thread.resume()
                self.pause_btn.setText("Pause")
                self.is_paused = False
            else:
                # Pause
                self.dictation_thread.pause()
                self.pause_btn.setText("Resume")
                self.is_paused = True

    def stop_dictation(self):
        """Stop the dictation thread"""
        if self.dictation_thread:
            self.dictation_thread.stop()
            self.dictation_thread = None

            # Update button states
            self.start_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)
            self.pause_btn.setText("Pause")
            self.is_paused = False

    def append_text(self, text):
        """Add transcribed text to the display"""
        # Move cursor to end
        cursor = self.text_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.text_display.setTextCursor(cursor)

        # Append text with a space
        self.text_display.insertPlainText(text + " ")

    def clear_text(self):
        """Clear all text from the display"""
        self.text_display.clear()
