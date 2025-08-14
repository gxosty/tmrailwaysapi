import datetime


class RWJourney:
    __slots__ = [
        "id",
        "source",
        "destination",
        "departure_time",
        "arrival_time",
        "travel_time",
        "train_run_number",
        "service_type_id",
        "service_type_title",
        "distance",
    ]

    def __init__(
        self,
        id: int,
        source: str,
        destination: str,
        departure_time: datetime.datetime,
        arrival_time: datetime.datetime,
        travel_time: int,
        train_run_number: str,
        service_type_id: int,
        service_type_title: str,
        distance: int,
    ) -> None:
        self.id = id
        self.source = source
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.travel_time = travel_time
        self.train_run_number = train_run_number
        self.service_type_id = service_type_id
        self.service_type_title = service_type_title
        self.distance = distance
