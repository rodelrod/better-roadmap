import os
from pathlib import Path

import yaml
from pydantic import BaseModel

APP_DIR = Path(os.getenv("APP_DIR", ".")).resolve()
DEFAULT_ELAPSED_FILE = APP_DIR / "data" / "default_elapsed.yml"


class ElapsedSprintSpan(BaseModel):
    start: int
    end: int


class ElapsedFeature(BaseModel):
    name: str
    elapsed: dict[str, ElapsedSprintSpan]


class ElapsedFeatureList(list[ElapsedFeature]):
    @classmethod
    def from_text(cls, elapsed_text):
        if not elapsed_text:
            elapsed_text = cls.get_default_elapsed_text()
        elapsed_as_dict = yaml.safe_load(elapsed_text)
        return [ElapsedFeature(**a) for a in elapsed_as_dict]

    @staticmethod
    def get_default_elapsed_text() -> str:
        with DEFAULT_ELAPSED_FILE.open() as elapsed_file:
            default_elapsed = elapsed_file.read()
        return default_elapsed
