from dataclasses import dataclass
from typing import Optional

from config import Config


@dataclass
class Feature(Config):
    name: str
    ux_estimation: int
    dev_estimation: int
    conception_estimation: Optional[int] = None
    ux_scheduled_sprint: Optional[int] = None
    conception_scheduled_sprint: Optional[int] = None
    dev_scheduled_sprint: Optional[int] = None
