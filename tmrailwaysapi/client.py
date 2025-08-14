import json
from typing import Optional, List

from .session import RWSession
from .constants import RWConstants
from .models import RWLocation
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
            location = RWLocation(id=str(station["id"]), name=station["title_tm"])
            self._locations.append(location)

    @property
    def locations(self) -> List[RWLocation]:
        if not self._locations:
            self._fetch_locations()
        return self._locations

    def get_location_by_id(self, location_id: str) -> Optional[RWLocation]:
        """Gets location by id"""
        for location in self.locations:
            if location.id == location_id:
                return location

        return None

