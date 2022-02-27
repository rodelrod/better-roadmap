import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

from ..config import Config

APP_DIR = Path(os.getenv("APP_DIR", ".")).resolve()
DEFAULT_FEATURES_FILE = APP_DIR / "data" / "default_features.yml"


@dataclass
class Feature(Config):
    name: str
    estimations: dict[str, int]
    real_start: Optional[dict[str, int]] = None
    real_duration: Optional[dict[str, int]] = None


class FeatureList(list[Feature]):
    @classmethod
    def from_text(cls, features_text):
        if not features_text:
            features_text = cls.get_default_features_text()
        feature_dicts = yaml.safe_load(features_text)
        features = [Feature.from_dict(d) for d in feature_dicts]
        return features

    @staticmethod
    def get_default_features_text() -> str:
        with DEFAULT_FEATURES_FILE.open() as features_file:
            default_features = features_file.read()
        return default_features
