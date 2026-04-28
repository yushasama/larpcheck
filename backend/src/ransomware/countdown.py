import time

from ransomware.config import (
    DEADLINE_SECONDS,
    MINUTES_PER_HOUR,
    SECONDS_PER_MINUTE,
    ZERO_DEADLINE,
    ZERO_TIME,
)


class Countdown:
    def __init__(self, seconds: int = DEADLINE_SECONDS, started_at: float | None = None):
        self.seconds = seconds
        self.started_at = started_at if started_at is not None else time.time()

    def remaining(self) -> float:
        remaining_seconds = self.seconds - (time.time() - self.started_at)

        return max(0.0, remaining_seconds)

    def display(self) -> str:
        total_seconds = int(self.remaining())

        minutes, seconds = divmod(total_seconds, SECONDS_PER_MINUTE)

        if total_seconds <= 0:
            return ZERO_TIME

        return f"{minutes:02d}:{seconds:02d}"

    def deadline_display(self, deadline_seconds: int) -> str:
        remaining_seconds = max(0, deadline_seconds - int(time.time() - self.started_at))

        if remaining_seconds <= 0:
            return ZERO_DEADLINE

        hours, remainder = divmod(remaining_seconds, SECONDS_PER_MINUTE * MINUTES_PER_HOUR)

        minutes, seconds = divmod(remainder, SECONDS_PER_MINUTE)

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
