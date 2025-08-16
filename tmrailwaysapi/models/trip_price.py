import datetime
from typing import NamedTuple, List

from .journey_price import RWJourneyPrice


class RWTripPrice(NamedTuple):
    id: int
    arrival_time: datetime.datetime
    departure_time: datetime.datetime
    source: str
    destination: str
    distance: int
    journeys: List[RWJourneyPrice]
    travel_time: int
