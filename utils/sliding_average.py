class SlidingAverage:
    """Keep a fixed-size window and return the mean of the latest samples."""

    def __init__(self, window_size=5):
        if window_size <= 0:
            raise ValueError("window_size must be greater than zero")

        self.window_size = window_size
        self._values = []

    def add(self, value):
        self._values.append(float(value))
        if len(self._values) > self.window_size:
            self._values.pop(0)
        return self.get_average()

    def get_average(self):
        if not self._values:
            return 0.0
        return round(sum(self._values) / len(self._values), 4)

    def clear(self):
        self._values.clear()

    def __len__(self):
        return len(self._values)