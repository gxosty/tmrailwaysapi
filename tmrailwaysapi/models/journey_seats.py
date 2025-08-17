import datetime
from typing import NamedTuple, List

from .wagon_seats import RWWagonSeats

class RWJourneySeats(NamedTuple):
    id: int
    arrival_time: datetime.datetime
    departure_time: datetime.datetime
    source: str
    destination: str
    distance: int
    service_type_id: int
    service_type_title: str
    train_run_number: int
    travel_time: int
    train_wagons: List[RWWagonSeats]
