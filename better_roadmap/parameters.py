import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

from .config import Config

APP_DIR = Path(os.getenv("APP_DIR", ".")).resolve()
DEFAULT_PARAMETERS_FILE = APP_DIR / "data" / "default_parameters.yml"


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

    @classmethod
    def from_text(cls, parameters_text: Optional[str]):
        if not parameters_text:
            parameters_text = cls.get_default_parameters_text()
        parameters_dict = yaml.safe_load(parameters_text)
        parameters = cls.from_dict(
            {
                "project_start": parameters_dict["project_start"],
                "default_sprint_duration": parameters_dict["default_sprint_duration"],
                "phases": [Phase.from_dict(p) for p in parameters_dict["phases"]],
                "sprint_durations": [
                    SprintDuration.from_dict(s) for s in parameters_dict["sprints"]
                ],
            }
        )
        return parameters

    @staticmethod
    def get_default_parameters_text() -> str:
        with DEFAULT_PARAMETERS_FILE.open() as parameters_file:
            default_parameters = parameters_file.read()
        return default_parameters
