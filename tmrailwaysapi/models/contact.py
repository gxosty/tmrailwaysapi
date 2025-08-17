from typing import NamedTuple


class RWContact(NamedTuple):
    mobile: str # "+993xxxxxxxx"
    email: str
    main_contact: str # f"{passenger.name} {passenger.surname}"
