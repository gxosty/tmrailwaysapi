import datetime
from typing import List

from .wagon import RWWagon
from .journey import RWJourney


class RWTrip:
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

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"<RWTrip: from '{self.source}' to '{self.destination}'>"

    def get_available_wagons(self) -> List[RWWagon]:
        available_wagons = []

        for wagon in self.wagon_types:
            if wagon.has_seats:
                available_wagons.append(wagon)

        return available_wagons
