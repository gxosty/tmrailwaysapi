from typing import NamedTuple, List, Optional

from .trip_price import RWTripPrice
from .price import RWPrice


class RWPriceSummary(NamedTuple):
    outbound: RWTripPrice
    inbound: Optional[RWTripPrice]
    price_formation: List[RWPrice]
