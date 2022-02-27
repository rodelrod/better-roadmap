from dataclasses import dataclass


@dataclass
class Config:
    @classmethod
    def from_dict(cls, d: dict):
        return cls(**d)
