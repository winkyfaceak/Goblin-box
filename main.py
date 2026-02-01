import sys

from audio import recorder
from stt import whisper_engine
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
from PyQt6.QtWidgets import QApplication
from ui.core import MainWindow



def main():

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

    # while True:
    #     try:
    #         audio = recorder.AudioRecorder().record(duration=5)
    #         text = whisper_engine.WhisperEngine(model_size="base").transcribe(audio_np=audio)
    #
    #         if text:
    #             print(f"Transcribed Text: {text}")
    #
    #     except KeyboardInterrupt:
    #         print("Exiting...")
    #         break


if __name__ == "__main__":
    main()