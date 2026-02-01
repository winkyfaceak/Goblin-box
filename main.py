from audio import recorder
from stt import whisper_engine
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

def main():

    while True:
        try:
            audio = recorder.AudioRecorder().record(duration=5)
            text = whisper_engine.WhisperEngine(model_size="base").transcribe(audio_np=audio)

            if text:
                print(f"Transcribed Text: {text}")

        except KeyboardInterrupt:
            print("Exiting...")
            break


if __name__ == "__main__":
    main()