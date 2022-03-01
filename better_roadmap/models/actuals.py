import os
from dataclasses import dataclass
from pathlib import Path

import yaml

from .config import Config

APP_DIR = Path(os.getenv("APP_DIR", ".")).resolve()
DEFAULT_ACTUAL_FILE = APP_DIR / "data" / "default_actuals.yml"


@dataclass
class ActualSprintSpan(Config):
    start: int
    end: int


@dataclass
class ActualFeature(Config):
    name: str
    actual: dict[str, ActualSprintSpan]


class ActualFeatureList(list[ActualFeature]):
    @classmethod
    def from_text(cls, actuals_text):
        if not actuals_text:
            actuals_text = cls.get_default_actuals_text()
        actual_feature_dict_list = yaml.safe_load(actuals_text)
        actual_feature_list = cls()
        print("afdl: ", actual_feature_dict_list)
        for actual_feature_dict in actual_feature_dict_list:
            print("adf: ", actual_feature_dict)
            name = actual_feature_dict["name"]
            actual_dict = actual_feature_dict["actual"]
            actual = dict()
            for phase, span in actual_dict.items():
                actual_sprint_span = ActualSprintSpan.from_dict(span)
                actual[phase] = actual_sprint_span
            actual_feature_list.append(ActualFeature(name, actual))

        return actual_feature_list

    @staticmethod
    def get_default_actuals_text() -> str:
        with DEFAULT_ACTUAL_FILE.open() as actual_file:
            default_actuals = actual_file.read()
        return default_actuals
