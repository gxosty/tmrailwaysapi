import datetime
from typing import List

from .wagon import RWWagon
from .journey import RWJourney


class RWTrip:
    __slots__ = [
        "id",
        "source",
        "destination",
        "departure_time",
        "arrival_time",
        "travel_time",
        "distance",
        "wagon_types",
        "journeys",
    ]

    def __init__(
        self,
        id: int,
        source: str,
        destination: str,
        departure_time: datetime.datetime,
        arrival_time: datetime.datetime,
        travel_time: int,
        distance: int,
        wagon_types: List[RWWagon],
        journeys: List[RWJourney],
    ) -> None:
        self.id = id
        self.source = source
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.travel_time = travel_time
        self.distance = distance
        self.wagon_types = wagon_types
        self.journeys = journeys
