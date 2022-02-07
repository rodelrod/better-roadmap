from dataclasses import dataclass
from typing import Optional


@dataclass
class Feature:
    name: str
    ux_estimation: int
    dev_estimation: int
    conception_estimation: Optional[int] = None
    ux_scheduled_sprint: Optional[int] = None
    conception_scheduled_sprint: Optional[int] = None
    dev_scheduled_sprint: Optional[int] = None

    @classmethod
    def from_dict(cls, d: dict):
        return cls(**d)
