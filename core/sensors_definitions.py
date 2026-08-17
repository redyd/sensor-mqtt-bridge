from typing import Protocol


class TemperatureSensor(Protocol):
    def get_temperature(self) -> tuple[float, float]: ...


class PressureSensor(Protocol):
    def get_pressure(self) -> tuple[float, float]: ...


class HumiditySensor(Protocol):
    def get_humidity(self) -> tuple[float, float]: ...


class LightSensor(Protocol):
    def get_light(self) -> tuple[float, float]: ...


class MicrophoneSensor(Protocol):
    def get_sound_level(self) -> tuple[float, float]: ...


class ParticulateMatterSensor(Protocol):
    def get_particulate_matter(self) -> tuple[float, float]: ...


class Co2Sensor(Protocol):
    def get_co2(self) -> tuple[float, float]: ...
