from typing import TypeVar

T = TypeVar("T")


def index_min(lst: list):
    return min(range(len(lst)), key=lst.__getitem__)


def replace_min(lst: list[T], value: T):
    lst[index_min(lst)] = value
