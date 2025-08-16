import datetime
from typing import NamedTuple, List

from .wagon_price import RWWagonPrice


class RWJourneyPrice(NamedTuple):
    id: int
    arrival_time: datetime.datetime
    departure_time: datetime.datetime
    source: str
    destination: str
    distance: int
    prices: List[RWWagonPrice]
    service_type_id: int
    service_type_title: str
    train_run_number: int
    travel_time: int
