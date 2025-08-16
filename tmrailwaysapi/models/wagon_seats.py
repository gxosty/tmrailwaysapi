from typing import NamedTuple, List

from .seat import RWSeat


class RWWagonSeats(NamedTuple):
    id: int
    layout_map: str
    number: int
    seats: List[RWSeat]
    wagon_type_id: int
    wagon_type_title: str

