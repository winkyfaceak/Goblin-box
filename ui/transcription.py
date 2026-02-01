import librosa
from PyQt6.QtCore import pyqtSignal, QThread
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout, QFileDialog, QLabel

from stt import whisper_engine


class TranscriptionThread(QThread):
    """Background thread for file transcription"""
    transcription_complete = pyqtSignal(str)
    transcription_error = pyqtSignal(str)

    def __init__(self, audio_file_path):
        super().__init__()
        self.audio_file_path = audio_file_path
        self.whisper = whisper_engine.WhisperEngine(model_size="base")

    def run(self):
        try:
            audio, sr = librosa.load(self.audio_file_path, sr=16000)
            text = self.whisper.transcribe(audio_np=audio)

            if text:
                self.transcription_complete.emit(text)
            else:
                self.transcription_error.emit("No text transcribed")
        except Exception as e:
            self.transcription_error.emit(str(e))


class TranscriptionPage(QWidget):
    """Transcription page - upload audio files and transcribe them"""
    switch_page = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Audio Transcription")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Status
        self.status_label = QLabel("Upload an audio file to transcribe")

        # Upload button
        upload_btn = QPushButton("📁 Upload Audio File")
        upload_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        upload_btn.clicked.connect(self.upload_file)

        # Text display
        self.text_display = QTextEdit()
        self.text_display.setPlaceholderText("Transcribed text will appear here...")
        self.text_display.setMinimumHeight(400)

        # Utility buttons
        utility_layout = QHBoxLayout()

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_text)

        save_btn = QPushButton("Save to File")
        save_btn.clicked.connect(self.save_to_file)

        utility_layout.addWidget(clear_btn)
        utility_layout.addWidget(save_btn)

        # Back button
        back_btn = QPushButton("← Back to Home")
        back_btn.clicked.connect(lambda: self.switch_page.emit("home"))

        # Layout
        layout.addWidget(title)
        layout.addWidget(self.status_label)
        layout.addWidget(upload_btn)
        layout.addWidget(self.text_display)
        layout.addLayout(utility_layout)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

        self.transcription_thread = None

    def upload_file(self):
        """Open file picker and transcribe selected file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.wav *.mp3 *.m4a *.flac *.ogg *.opus);;All Files (*.*)"
        )

        if file_path:
            filename = file_path.split('/')[-1]
            self.status_label.setText(f"Transcribing: {filename}...")
            self.text_display.clear()

            # Start transcription
            self.transcription_thread = TranscriptionThread(file_path)
            self.transcription_thread.transcription_complete.connect(self.on_complete)
            self.transcription_thread.transcription_error.connect(self.on_error)
            self.transcription_thread.start()

    def on_complete(self, text):
        """Called when transcription finishes"""
        self.text_display.setPlainText(text)
        self.status_label.setText("✓ Transcription complete!")

    def on_error(self, error_msg):
        """Called when transcription fails"""
        self.status_label.setText(f"✗ Error: {error_msg}")
        self.text_display.setPlainText(f"Error:\n{error_msg}")

    def clear_text(self):
        """Clear text display"""
        self.text_display.clear()
        self.status_label.setText("Text cleared")

    def save_to_file(self):
        """Save transcription to file"""
        text = self.text_display.toPlainText()

        if not text:
            self.status_label.setText("No text to save")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Transcription",
            "transcription.txt",
            "Text Files (*.txt);;All Files (*.*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                filename = file_path.split('/')[-1]
                self.status_label.setText(f"✓ Saved to {filename}")
            except Exception as e:
                self.status_label.setText(f"✗ Error: {str(e)}")