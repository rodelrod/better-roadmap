from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from config import Config


@dataclass
class Phase(Config):
    name: str
    valid_from: datetime
    max_concurrency: int
    min_gap: int
    max_gap: Optional[int] = None
    default_estimation: Optional[int] = None


@dataclass
class Sprint(Config):
    number: int
    duration: int


@dataclass
class Parameters(Config):
    project_start: datetime
    default_sprint_duration: int
    phases: list[Phase]
    sprints: list[Sprint]
