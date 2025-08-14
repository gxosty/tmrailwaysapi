import datetime
from typing import Dict, Any

from .models import RWLocation, RWTrip, RWWagon, RWJourney


def location_from_json(json_data: Dict[str, Any]) -> RWLocation:
    location = RWLocation(id=json_data["id"], name=json_data["title_tm"])
    return location


def wagon_from_json(json_data: Dict[str, Any]) -> RWWagon:
    wagon = RWWagon(
        id=json_data["wagon_type_id"],
        title=json_data["wagon_type_title"],
        price=json_data["price"],
        has_seats=json_data["has_seats"],
    )
    return wagon


def journey_from_json(json_data: Dict[str, Any]) -> RWJourney:
    journey = RWJourney(
        id=json_data["id"],
        source=json_data["source"],
        destination=json_data["destination"],
        departure_time=datetime.datetime.fromisoformat(json_data["departure_time"]),
        arrival_time=datetime.datetime.fromisoformat(json_data["arrival_time"]),
        travel_time=json_data["travel_time"],
        train_run_number=json_data["train_run_number"],
        service_type_id=json_data["service_type_id"],
        service_type_title=json_data["service_type_title"],
        distance=json_data["distance"],
    )
    return journey


def trip_from_json(json_data: Dict[str, Any]) -> RWTrip:
    wagons = []
    journeys = []

    for wagon_type in json_data["wagon_types"]:
        wagon = wagon_from_json(wagon_type)
        wagons.append(wagon)

    for journey_data in json_data["journeys"]:
        journey = journey_from_json(journey_data)
        journeys.append(journey)

    return RWTrip(
        id=json_data["id"],
        source=json_data["source"],
        destination=json_data["destination"],
        departure_time=datetime.datetime.fromisoformat(json_data["departure_time"]),
        arrival_time=datetime.datetime.fromisoformat(json_data["arrival_time"]),
        travel_time=json_data["travel_time"],
        distance=json_data["distance"],
        wagon_types=wagons,
        journeys=journeys,
    )
