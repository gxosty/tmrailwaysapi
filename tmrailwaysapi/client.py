from typing import Optional, List

from .session import RWSession
from .constants import RWConstants
from .parser import RWParser
from .models import RWLocation


class RWClient:
    def __init__(self, hostname: Optional[str] = None) -> None:
        hostname = hostname or RWConstants.HOSTNAME
        self._session = RWSession(hostname=hostname)
        self._src_locations = []
        self._dest_locations = []

        self._fetch_locations()

    def _fetch_locations(self) -> None:
        response = self._session.get_main_page()
        self._src_locations, self._dest_locations = RWParser.parse_locations(
            response.text
        )

    @property
    def src_locations(self) -> List[RWLocation]:
        return self._src_locations

    @property
    def dest_locations(self) -> List[RWLocation]:
        return self._dest_locations
