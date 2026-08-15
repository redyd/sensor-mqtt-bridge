import numpy
import sounddevice

from core.sensors_definitions import MicrophoneSensor
from utils.sliding_average import SlidingAverage


class Sph0645Sensor(MicrophoneSensor):
    """SPH0645LM4H-B: microphone."""

    def __init__(self, samplerate=48000, duration=0.5):
        self._samplerate = samplerate
        self._duration = duration
        self._sound_level_average = SlidingAverage()

    def get_sound_level(self) -> tuple[float, float]:
        recording = sounddevice.rec(
            int(self._duration * self._samplerate),
            samplerate=self._samplerate,
            channels=1,
            dtype="float32",
        )
        sounddevice.wait()
        raw = float(numpy.sqrt(numpy.mean(numpy.square(recording))))
        return raw, self._sound_level_average.add(raw)
