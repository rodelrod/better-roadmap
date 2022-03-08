import os
from datetime import date
from pathlib import Path
from pydantic import BaseModel
from typing import Optional

import yaml

from .config_type import ConfigType


APP_DIR = Path(os.getenv("APP_DIR", ".")).resolve()
DEFAULT_PARAMETERS_FILE = APP_DIR / "data" / "default_parameters.yml"


class Phase(BaseModel):
    name: str
    max_concurrency: int
    min_gap_before: int
    max_gap_after: Optional[int] = None
    default_estimation: Optional[int] = None
    valid_from_sprint: int = 1


class SprintDuration(BaseModel):
    number: int
    duration: int


class Parameters(ConfigType, BaseModel):
    project_start: date
    default_sprint_duration: int
    phases: list[Phase]
    sprint_durations: Optional[list[SprintDuration]] = None
    next_milestone: Optional[date] = None

    @classmethod
    def from_text(cls, parameters_text: Optional[str]):
        if not parameters_text:
            parameters_text = cls.get_default_text()
        parameters_dict = yaml.safe_load(parameters_text)
        return cls(**parameters_dict)

    @staticmethod
    def get_default_text() -> str:
        with DEFAULT_PARAMETERS_FILE.open() as parameters_file:
            default_parameters = parameters_file.read()
        return default_parameters
