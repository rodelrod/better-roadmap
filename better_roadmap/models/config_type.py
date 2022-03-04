from abc import ABC, abstractmethod


class ConfigType(ABC):
    @classmethod
    @abstractmethod
    def from_text(cls, config_text: str):
        pass

    @staticmethod
    @abstractmethod
    def get_default_text() -> str:
        pass
