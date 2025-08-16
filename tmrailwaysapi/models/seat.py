from typing import NamedTuple


class RWSeat(NamedTuple):
    id: int
    available: bool
    label: str
    level: int
