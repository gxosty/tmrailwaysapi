import datetime
from typing import Optional, List

from . import model_mappers
from .session import RWSession
from .constants import RWConstants
from .models import RWLocation, RWTrip
from .exceptions import APIStatusError


class RWClient:
    """Main client to interract with Turkmenistan Railways"""

    def __init__(self, hostname: Optional[str] = None) -> None:
        hostname = hostname or RWConstants.HOSTNAME
        self._session = RWSession(hostname=hostname)

        self._locations = []

    def _fetch_locations(self) -> None:
        """Fetch stations/locations"""
        response = self._session.get_stations()
        json_data = response.json()
        APIStatusError.raise_for_status(json_data)

        for station in json_data["data"]["stations"]:
            location = model_mappers.location_from_json(station)
            self._locations.append(location)

    @property
    def locations(self) -> List[RWLocation]:
        if not self._locations:
            self._fetch_locations()
        return self._locations

    def get_location_by_id(self, location_id: int) -> Optional[RWLocation]:
        """Gets location by id"""
        for location in self.locations:
            if location.id == location_id:
                return location

        return None

    def get_location_by_name(self, location_name: str) -> Optional[RWLocation]:
        """Gets location by name"""
        for location in self.locations:
            if location.name == location_name:
                return location

        return None

    def search_trips(
        self,
        src_location: RWLocation,
        dest_location: RWLocation,
        date: datetime.datetime,
        adults: int,
        children: int = 0,
    ) -> List[RWTrip]:
        """Search trips by given critteria"""
        date_str = date.strftime("%Y-%m-%d")

        response = self._session.search_trips(
            src_location.id,
            dest_location.id,
            date_str,
            adults,
            children,
        )
        response_json = response.json()
        APIStatusError.raise_for_status(response_json)
        trips = []

        for trip_data in response_json["data"]["trips"]:
            trip = model_mappers.trip_from_json(trip_data)
            trips.append(trip)

        return trips
