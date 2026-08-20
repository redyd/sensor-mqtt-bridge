import numpy as np
import sounddevice as sd

from core.sensors_definitions import MicrophoneSensor
from utils.sliding_average import SlidingAverage


class Sph0645Sensor(MicrophoneSensor):
    """SPH0645LM4H-B: microphone."""

    def __init__(self, samplerate: int = 48000, duration: float = 0.5) -> None:
        self._samplerate = samplerate
        self._duration = duration
        self._sound_level_average = SlidingAverage()

    def get_sound_level(self) -> tuple[float, float]:
        recording = sd.rec(
            int(self._duration * self._samplerate),
            samplerate=self._samplerate,
            channels=1,
            dtype="float32",
        )
        sd.wait()  # blocks until the recording buffer is full
        # RMS amplitude as a proxy for sound pressure level
        raw = float(np.sqrt(np.mean(np.square(recording))))
        return raw, self._sound_level_average.add(raw)
