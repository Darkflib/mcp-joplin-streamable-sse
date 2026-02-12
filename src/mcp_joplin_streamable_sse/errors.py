"""Domain errors."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JoplinApiError(RuntimeError):
    """Raised when the Joplin Data API returns a non-success response."""

    status_code: int
    method: str
    url: str
    response_text: str

    def __str__(self) -> str:  # pragma: no cover
        return (
            f"Joplin API error {self.status_code} for {self.method} {self.url}: "
            f"{self.response_text}"
        )
