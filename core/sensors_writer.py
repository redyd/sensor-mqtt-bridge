import csv
import os
from typing import ClassVar

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sensors.csv")


class SensorsCsvWriter:
    """Write smoothed sensor values and the global score to a CSV file."""

    FIELDNAMES: ClassVar[list[str]] = [
        "timestamp",
        "temperature",
        "pressure",
        "humidity",
        "light",
        "sound_level",
        "particulate_matter",
        "co2",
        "score",
    ]

    def __init__(self, path: str = DEFAULT_PATH):
        self._path = path
        directory = os.path.dirname(self._path)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def write(self, payload: dict) -> None:
        file_exists = os.path.isfile(self._path)
        file_is_empty = not file_exists or os.path.getsize(self._path) == 0  # write header only if file is new or empty

        with open(self._path, "a", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.FIELDNAMES)
            if file_is_empty:
                writer.writeheader()
            writer.writerow(self._build_row(payload))

    def _build_row(self, payload: dict) -> dict[str, object]:
        values = payload["values"]
        row = {
            "timestamp": payload["timestamp"],
            "score": payload.get("score"),
        }

        for key in self.FIELDNAMES:
            if key in ("timestamp", "score"):
                continue
            reading = values.get(key)
            row[key] = reading["smooth"] if reading is not None else None

        return row
