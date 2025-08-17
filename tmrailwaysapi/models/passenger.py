import datetime
from typing import NamedTuple


class RWPassenger(NamedTuple):
    name: str
    surname: str
    dob: datetime.datetime # "DD-MM-YYYY"
    tariff: str # "adult"
    gender: str # "male"
    identity_type: str # "passport"
    identity_number: str # "I-AS XXXXXX"
