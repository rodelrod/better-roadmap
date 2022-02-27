import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

from .config import Config

APP_DIR = Path(os.getenv("APP_DIR", ".")).resolve()
PARAMETERS_FILE = APP_DIR / "data" / "parameters.yml"


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


def parse_parameters(parameters_text) -> Parameters:
    if parameters_text:
        parameters_dict = yaml.safe_load(parameters_text)
    else:
        with PARAMETERS_FILE.open() as parameters_file:
            parameters_dict = yaml.safe_load(parameters_file)
    parameters = Parameters.from_dict(
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


def get_default_parameters_as_text() -> str:
    with PARAMETERS_FILE.open() as parameters_file:
        default_parameters = parameters_file.read()
    return default_parameters
