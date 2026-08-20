"""Structural (Protocol) interfaces for all sensor types used in the bridge."""

from typing import Protocol

SensorReading = tuple[float, float]  # (raw, smoothed)


class TemperatureSensor(Protocol):
    def get_temperature(self) -> SensorReading: ...


class PressureSensor(Protocol):
    def get_pressure(self) -> SensorReading: ...


class HumiditySensor(Protocol):
    def get_humidity(self) -> SensorReading: ...


class LightSensor(Protocol):
    def get_light(self) -> SensorReading: ...


class MicrophoneSensor(Protocol):
    def get_sound_level(self) -> SensorReading: ...


class ParticulateMatterSensor(Protocol):
    def get_particulate_matter(self) -> SensorReading: ...


class Co2Sensor(Protocol):
    def get_co2(self) -> SensorReading: ...
