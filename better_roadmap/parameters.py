from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .config import Config


@dataclass
class Phase(Config):
    name: str
    max_concurrency: int
    min_gap_before: int
    max_gap_after: Optional[int] = None
    default_estimation: Optional[int] = None
    valid_from_sprint: int = 1


@dataclass
class SprintDuration(Config):
    number: int
    duration: int


@dataclass
class Parameters(Config):
    project_start: datetime
    default_sprint_duration: int
    phases: list[Phase]
    sprint_durations: Optional[list[SprintDuration]] = None


DEFAULT_PARAMETERS = Parameters(
    datetime(2022, 10, 1),
    1,
    phases=[
        Phase("ux", 1, 0),
        Phase("conception", 2, 0, 3, 1),
        Phase("dev", 2, 1),
    ],
)
