from typing import NamedTuple, List

from .journey_seats import RWJourneySeats


class RWTripSeats(NamedTuple):
    id: int
    journeys: List[RWJourneySeats]
