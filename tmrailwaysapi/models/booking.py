import datetime
from typing import NamedTuple


class RWBooking(NamedTuple):
    booking_number: str
    expire_time: datetime.datetime
    order_number: str
    form_url: str
