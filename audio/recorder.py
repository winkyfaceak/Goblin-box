import time
from queue import Queue, Empty
import numpy as np
import sounddevice as sd

class AudioRecorder:
    """
    Simple audio recorder that collects input blocks into a Queue.
    Returns a float32 mono numpy array normalized to [-1.0, 1.0].
    """

    def __init__(self, samplerate: int = 16000, channels: int = 1, dtype: str = 'int16', blocksize: int = 1024):
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self.blocksize = blocksize
        self.queue = Queue()
        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            blocksize=self.blocksize,
            callback=self._callback
        )

    def _callback(self, indata, frames, time_, status):
        if status:
            # keep short and non-blocking
            print("AudioRecorder status:", status)
        # copy to avoid referencing the shared buffer
        self.queue.put(indata.copy())

    def record(self, duration: float = 5.0) -> np.ndarray:
        """Record for `duration` seconds and return mono float32 numpy array."""
        frames = []
        self.stream.start()
        end_time = time.time() + float(duration)
        try:
            while time.time() < end_time:
                timeout = max(0.1, end_time - time.time())
                try:
                    block = self.queue.get(timeout=timeout)
                    frames.append(block)
                except Empty:
                    # nothing arrived in this interval; continue until duration elapsed
                    continue
        finally:
            self.stream.stop()

        if not frames:
            return np.empty((0,), dtype=np.float32)

        audio_np = np.concatenate(frames, axis=0)  # shape (n_samples, channels)
        # convert integer audio to float32 normalized to [-1, 1]
        if np.issubdtype(audio_np.dtype, np.integer):
            max_val = np.iinfo(audio_np.dtype).max
            audio = audio_np.astype(np.float32) / float(max_val)
        else:
            audio = audio_np.astype(np.float32)

        # convert to mono by averaging channels if necessary
        if audio.ndim > 1 and audio.shape[1] > 1:
            audio = audio.mean(axis=1)

        return audio.squeeze()