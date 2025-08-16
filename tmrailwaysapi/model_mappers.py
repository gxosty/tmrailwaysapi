import datetime
from typing import Dict, Any

from .models import (
    RWJourney,
    RWJourneyPrice,
    RWJourneySeats,
    RWLocation,
    RWPrice,
    RWPriceSummary,
    RWSeat,
    RWSeats,
    RWTrip,
    RWTripPrice,
    RWTripSeats,
    RWWagon,
    RWWagonPrice,
    RWWagonSeats,
)


def location_from_json(json_data: Dict[str, Any]) -> RWLocation:
    location = RWLocation(id=json_data["id"], name=json_data["title_tm"])
    return location


def wagon_from_json(json_data: Dict[str, Any]) -> RWWagon:
    return RWWagon(
        id=json_data["wagon_type_id"],
        title=json_data["wagon_type_title"],
        price=json_data["price"],
        has_seats=json_data["has_seats"],
    )


def journey_from_json(json_data: Dict[str, Any]) -> RWJourney:
    return RWJourney(
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


def wagon_price_from_json(json_data: Dict[str, Any]) -> RWWagonPrice:
    return RWWagonPrice(
        id=json_data["wagon_type_id"],
        title=json_data["wagon_type_title"],
        adult=json_data["adult"],
        child=json_data.get("child", 0),
    )


def journey_price_from_json(json_data: Dict[str, Any]) -> RWJourneyPrice:
    wagon_prices = []

    for wagon_price_data in json_data["prices"]:
        wagon_price = wagon_price_from_json(wagon_price_data)
        wagon_prices.append(wagon_price)

    return RWJourneyPrice(
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
        prices=wagon_prices,
    )


def trip_price_from_json(json_data: Dict[str, Any]) -> RWTripPrice:
    journey_prices = []

    for journey_price_data in json_data["journeys"]:
        journey_price = journey_price_from_json(journey_price_data)
        journey_prices.append(journey_price)

    return RWTripPrice(
        id=json_data["id"],
        source=json_data["source"],
        destination=json_data["destination"],
        departure_time=datetime.datetime.fromisoformat(json_data["departure_time"]),
        arrival_time=datetime.datetime.fromisoformat(json_data["arrival_time"]),
        travel_time=json_data["travel_time"],
        distance=json_data["distance"],
        journeys=journey_prices,
    )


def price_from_json(json_data: Dict[str, Any]) -> RWPrice:
    return RWPrice(
        id=json_data["id"], title=json_data["title"], amount=json_data["amount"]
    )


def price_summary_from_json(json_data: Dict[str, Any]) -> RWPriceSummary:
    outbound = trip_price_from_json(json_data["outbound"])
    inbound = (
        trip_price_from_json(json_data["inbound"]) if "inbound" in json_data else None
    )
    price_formation = []

    for price_data in json_data["price_formation"]:
        price = price_from_json(price_data)
        price_formation.append(price)

    return RWPriceSummary(
        outbound=outbound,
        inbound=inbound,
        price_formation=price_formation,
    )


def seat_from_json(json_data: Dict[str, Any]) -> RWSeat:
    return RWSeat(
        id=json_data["id"],
        available=json_data["available"],
        label=json_data["label"],
        level=int(json_data["level"]),
    )


def wagon_seats_from_json(json_data: Dict[str, Any]) -> RWWagonSeats:
    seats = []

    for seat_data in json_data["seats"]:
        seat = seat_from_json(seat_data)
        seats.append(seat)

    return RWWagonSeats(
        id=json_data["id"],
        layout_map=json_data["layout_map"],
        number=json_data["number"],
        seats=seats,
        wagon_type_id=json_data["wagon_type_id"],
        wagon_type_title=json_data["wagon_type_title"]
    )


def journey_seats_from_json(json_data: Dict[str, Any]) -> RWJourneySeats:
    train_wagons = []

    for wagon_seats_data in json_data["train_wagons"]:
        wagon_seats = wagon_seats_from_json(wagon_seats_data)
        train_wagons.append(wagon_seats)

    return RWJourneySeats(
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
        train_wagons=train_wagons,
    )


def trip_seats_from_json(json_data: Dict[str, Any]) -> RWTripSeats:
    journeys = []

    for journey_seats_data in json_data["journeys"]:
        journey_seats = journey_seats_from_json(journey_seats_data)
        journeys.append(journey_seats)

    return RWTripSeats(id=json_data["trip_id"], journeys=journeys)


def seats_from_json(json_data: Dict[str, Any]) -> RWSeats:
    outbound = trip_seats_from_json(json_data["outbound"])
    inbound = (
        trip_seats_from_json(json_data["inbound"]) if "inbound" in json_data else None
    )

    return RWSeats(outbound=outbound, inbound=inbound)
