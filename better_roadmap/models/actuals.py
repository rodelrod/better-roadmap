import os
from pathlib import Path

import yaml
from pydantic import BaseModel

APP_DIR = Path(os.getenv("APP_DIR", ".")).resolve()
DEFAULT_ACTUAL_FILE = APP_DIR / "data" / "default_actuals.yml"


class ActualSprintSpan(BaseModel):
    start: int
    end: int


class ActualFeature(BaseModel):
    name: str
    actual: dict[str, ActualSprintSpan]


class ActualFeatureList(list[ActualFeature]):
    @classmethod
    def from_text(cls, actuals_text):
        if not actuals_text:
            actuals_text = cls.get_default_actuals_text()
        actuals_as_dict = yaml.safe_load(actuals_text)
        return [ActualFeature(**a) for a in actuals_as_dict]

    @staticmethod
    def get_default_actuals_text() -> str:
        with DEFAULT_ACTUAL_FILE.open() as actual_file:
            default_actuals = actual_file.read()
        return default_actuals
