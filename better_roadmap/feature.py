from dataclasses import dataclass
from typing import Optional

from .config import Config


@dataclass
class Feature(Config):
    name: str
    estimations: dict[str, int]
    real_start: Optional[dict[str, int]] = None
    real_duration: Optional[dict[str, int]] = None
