import numpy
import sounddevice

from core.sensors_definitions import MicrophoneSensor


class Sph0645Sensor(MicrophoneSensor):
    """SPH0645LM4H-B : microphone."""

    def __init__(self, samplerate=48000, duration=0.5):
        self._samplerate = samplerate
        self._duration = duration

    def get_sound_level(self) -> float:
        recording = sounddevice.rec(
            int(self._duration * self._samplerate),
            samplerate=self._samplerate,
            channels=1,
            dtype="float32",
        )
        sounddevice.wait()
        rms = numpy.sqrt(numpy.mean(numpy.square(recording)))
        return float(rms)
