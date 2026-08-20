class SlidingAverage:
    """Keep a fixed-size window and return the mean of the latest samples."""

    def __init__(self, window_size: int = 5) -> None:
        if window_size <= 0:
            raise ValueError("window_size must be greater than zero")

        self.window_size = window_size
        self._values: list[float] = []

    def add(self, value: float) -> float:
        self._values.append(float(value))
        if len(self._values) > self.window_size:
            self._values.pop(0)  # evict oldest sample when window is full
        return self.get_average()

    def get_average(self) -> float:
        if not self._values:
            return 0.0
        return round(sum(self._values) / len(self._values), 4)  # 4 decimal places avoids float noise in display

    def clear(self) -> None:
        self._values.clear()

    def __len__(self) -> int:
        return len(self._values)
