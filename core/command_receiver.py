from collections.abc import Callable
from typing import ClassVar, final


@final
class CommandReceiver:
    """Dispatch of received MQTT commands."""

    SUBSCRIPTIONS: ClassVar[list[tuple[str, int]]] = [
        ("commands/interval", 2),  # QoS 2 = exactly-once delivery
        ("commands/pause", 2),
    ]

    def __init__(
        self,
        update_interval_callback: None | Callable[[int | float], None] = None,
        toggle_pause_callback: None | Callable[[bool], None] = None
    ):
        self._update_interval_callback = update_interval_callback
        self._toggle_pause_callback = toggle_pause_callback

        self._handlers = {
            "commands/interval": {
                "set_interval": self._handle_set_interval,
            },
            "commands/pause": {
                "toggle": self._toggle_pause,
            }
        }

    def handle(self, topic: str, payload: dict) -> None:
        command = payload.get("command")
        topic_handlers = self._handlers.get(topic, {})
        handler = topic_handlers.get(command, self._handle_unknown)
        handler(payload)

    def _handle_unknown(self, payload: dict) -> None:
        print(f"Unknown command: {payload}")

    def _handle_set_interval(self, payload: dict[str, int | float]) -> None:
        interval = payload.get("interval")

        if not isinstance(interval, (int, float)):
            print(f"Invalid interval value: {payload}")
            return

        if interval <= 0:
            print(f"Interval must be greater than zero: {interval}")
            return

        if self._update_interval_callback is not None:
            self._update_interval_callback(interval)

    def _toggle_pause(self, payload: dict[str, bool]) -> None:
        toggle = payload.get("toggle")

        if not isinstance(toggle, bool):
            print(f"Invalid pause value: {payload}")
            return

        if self._toggle_pause_callback is not None:
            self._toggle_pause_callback(toggle)
