import datetime
from typing import Optional, List, Any

from . import model_mappers
from .session import RWSession
from .constants import RWConstants
from .models import (
    RWContact,
    RWJourneySeats,
    RWLocation,
    RWPassenger,
    RWPriceSummary,
    RWSeat,
    RWTrip,
    RWTripSeats,
    RWWagon,
    RWWagonSeats,
)
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
            location = model_mappers.location_from_json(station)
            self._locations.append(location)

    @property
    def locations(self) -> List[RWLocation]:
        if not self._locations:
            self._fetch_locations()
        return self._locations

    def get_location_by_id(self, location_id: int) -> Optional[RWLocation]:
        """Gets location by id"""
        for location in self.locations:
            if location.id == location_id:
                return location

        return None

    def get_location_by_name(self, location_name: str) -> Optional[RWLocation]:
        """Gets location by name"""
        for location in self.locations:
            if location.name == location_name:
                return location

        return None

    def search_trips(
        self,
        src_location: RWLocation,
        dest_location: RWLocation,
        date: datetime.datetime,
        adults: int,
        children: int = 0,
    ) -> List[RWTrip]:
        """Search trips by given critteria"""
        date_str = date.strftime("%Y-%m-%d")

        response = self._session.search_trips(
            src_location.id,
            dest_location.id,
            date_str,
            adults,
            children,
        )
        response_json = response.json()
        APIStatusError.raise_for_status(response_json)
        trips = []

        for trip_data in response_json["data"]["trips"]:
            trip = model_mappers.trip_from_json(trip_data)
            trips.append(trip)

        return trips

    def get_price_summary(
        self, outbound_trip: RWTrip, inbound_trip: Optional[RWTrip] = None
    ) -> RWPriceSummary:
        """Get price summary for selected trips

        Actually this does not really give you price summary.
        All calculations has to be done manually on the client side.
        This only returns prices for services like how much for an adult or child.
        """

        response = self._session.get_price_summary(
            outbound_trip.id, inbound_trip.id if inbound_trip is not None else -1
        )
        response_json = response.json()
        APIStatusError.raise_for_status(response_json)
        return model_mappers.price_summary_from_json(response_json["data"])

    def get_seats(
        self,
        outbound_trip: RWTrip,
        outbound_wagon: RWWagon,
        adults: int,
        children: int = 0,
        inbound_trip: Optional[RWTrip] = None,
        inbound_wagon: Optional[RWWagon] = None,
    ) -> RWTripSeats:
        """Get available seats for given wagons/trains"""
        response = self._session.get_seats(
            outbound_trip.id,
            outbound_wagon.id,
            adults,
            children,
            inbound_trip.id if inbound_trip is not None else -1,
            inbound_wagon.id if inbound_wagon is not None else -1,
        )
        response_json = response.json()
        APIStatusError.raise_for_status(response_json)
        return model_mappers.seats_from_json(response_json["data"])

    def book_tickets(
        self,
        contact: RWContact,
        passengers: List[RWPassenger],
        outbound_journey: RWJourneySeats,
        outbound_wagon: RWWagonSeats,
        outbound_seat: RWSeat,
        has_media_wifi: bool = False,
        has_lunchbox: bool = False,
        bedding_type: str = "default",
        inbound_journey: Optional[RWJourneySeats] = None,
        inbound_wagon: Optional[RWWagonSeats] = None,
        inbound_seat: Optional[RWSeat] = None,
    ) -> Any:
        """Proceed to booking tickets

        Example request/response (just a reference):

        Request json:
        {
            "has_media_wifi": True,
            "has_lunchbox": False,
            "bedding_type": "default",
            "api_client": "web",
            "contact": {
                "mobile": "+99364232437",
                "email": "mben333@gmail.com",
                "main_contact": "Mathew Benedict",
            },
            "passengers": [
                {
                    "name": "Mathew",
                    "surname": "Benedict",
                    "dob": "17-03-1998",
                    "tariff": "adult",
                    "gender": "male",
                    "identity_type": "passport",
                    "identity_number": "I-AS 23247",
                }
            ],
            "outbound": {
                "selected_journeys": [
                    {"id": 7298282, "seats": [{"id": 73, "train_wagon_id": 350186}]}
                ]
            },
            "inbound": {
                "selected_journeys": [
                    {"id": 7311715, "seats": [{"id": 85, "train_wagon_id": 350259}]}
                ]
            },
        }

        Response json:
        {
            "success": True,
            "data": {
                "booking": {
                    "booking_number": "NKXNCZ",
                    "expire_time": "2025-08-17T18:14:46.547555+05:00",
                    "orderNumber": "NKXNCZ-17082025175946",
                    "formUrl": "https://mpi.gov.tm/payment/merchants/online/payment_ru.html?mdOrder=c03365ad-af93-4ccf-85d3-3d3a3ae129d5",
                }
            },
        }
        """

        if inbound_journey and inbound_wagon and inbound_seat:
            inbound_journey_id = inbound_journey.id
            inbound_wagon_id = inbound_wagon.id
            inbound_seat_id = inbound_seat.id
        elif inbound_journey or inbound_wagon or inbound_seat:
            raise ValueError(
                "You are trying to book tickets, but not all `inbound_*` arguments are set"
            )
        else:
            inbound_journey_id = inbound_wagon_id = inbound_seat_id = -1

        response = self._session.book_tickets(
            contact_mobile=contact.mobile,
            contact_email=contact.email,
            contact_main_contact=contact.main_contact,
            passengers=[
                {
                    "name": passenger.name,
                    "surname": passenger.surname,
                    "dob": passenger.dob,
                    "tariff": passenger.tariff,
                    "gender": passenger.gender,
                    "identity_type": passenger.identity_type,
                    "identity_number": passenger.identity_number,
                }
                for passenger in passengers
            ],
            outbound_journey_id=outbound_journey.id,
            outbound_wagon_id=outbound_wagon.id,
            outbound_seat_id=outbound_seat.id,
            api_client="web",
            has_media_wifi=has_media_wifi,
            has_lunchbox=has_lunchbox,
            bedding_type=bedding_type,
            inbound_journey_id=inbound_journey_id,
            inbound_wagon_id=inbound_wagon_id,
            inbound_seat_id=inbound_seat_id,
        )
        response_json = response.json()
        APIStatusError.raise_for_status(response_json)
        return model_mappers.booking_from_json(response_json["data"]["booking"])
