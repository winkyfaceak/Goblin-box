import numpy as np
import whisper


class WhisperEngine:
    def __init__(self, model_size="base"):
        # Load the Whisper model (e.g., "tiny", "base", "small", "medium", "large")
        self.model = whisper.load_model(model_size)
        # Set the model to evaluation mode

    def transcribe(self, audio_np):
        # Ensure audio is a 1D float32 numpy array
        audio_np = audio_np.flatten().astype(np.float32)
        # Normalize audio to the range [-1.0, 1.0]
        result = self.model.transcribe(
            audio_np,
            fp16=False)
        # Return the transcribed text
        return result["text"].strip()
