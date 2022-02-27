import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

from .config import Config

APP_DIR = Path(os.getenv("APP_DIR", ".")).resolve()
FEATURES_FILE = APP_DIR / "data" / "features.yml"


@dataclass
class Feature(Config):
    name: str
    estimations: dict[str, int]
    real_start: Optional[dict[str, int]] = None
    real_duration: Optional[dict[str, int]] = None


def parse_features(features_text) -> list[Feature]:
    if features_text:
        feature_dicts = yaml.safe_load(features_text)
    else:
        with FEATURES_FILE.open() as features_file:
            feature_dicts = yaml.safe_load(features_file)
    features = [Feature.from_dict(d) for d in feature_dicts]
    return features


def get_default_features_as_text() -> str:
    with FEATURES_FILE.open() as features_file:
        default_features = features_file.read()
    return default_features
