import os
from pathlib import Path

import yaml
from pydantic import BaseModel

APP_DIR = Path(os.getenv("APP_DIR", ".")).resolve()
DEFAULT_FEATURES_FILE = APP_DIR / "data" / "default_features.yml"


class Feature(BaseModel):
    name: str
    estimations: dict[str, int]


class FeatureList(list[Feature]):
    @classmethod
    def from_text(cls, features_text):
        if not features_text:
            features_text = cls.get_default_features_text()
        feature_dicts = yaml.safe_load(features_text)
        features = [Feature(**d) for d in feature_dicts]
        return features

    @staticmethod
    def get_default_features_text() -> str:
        with DEFAULT_FEATURES_FILE.open() as features_file:
            default_features = features_file.read()
        return default_features
