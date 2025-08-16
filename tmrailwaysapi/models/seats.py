from typing import NamedTuple, Optional

from .trip_seats import RWTripSeats


class RWSeats(NamedTuple):
    outbound: RWTripSeats
    inbound: Optional[RWTripSeats]
