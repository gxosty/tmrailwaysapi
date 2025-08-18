import datetime
from typing import Optional, List, Awaitable

from . import model_mappers
from .async_session import RWAsyncSession
from .constants import RWConstants
from .models import (
    RWBooking,
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


class RWAsyncClient:
    """The async version of RWClient"""

    def __init__(self, hostname: Optional[str] = None) -> None:
        hostname = hostname or RWConstants.HOSTNAME
        self._session = RWAsyncSession(hostname=hostname)

        self._locations = []

    async def _fetch_locations(self) -> Awaitable:
        """Fetch stations/locations"""
        response = await self._session.get_stations()
        json_data = await response.json()
        APIStatusError.raise_for_status(json_data)

        for station in json_data["data"]["stations"]:
            location = model_mappers.location_from_json(station)
            self._locations.append(location)

    async def close(self) -> Awaitable:
        # aiohttp.ClientSession has to be closed explicitly
        await self._session._close()

    async def get_locations(self) -> Awaitable[List[RWLocation]]:
        if not self._locations:
            await self._fetch_locations()
        return self._locations

    async def get_location_by_id(
        self, location_id: int
    ) -> Awaitable[Optional[RWLocation]]:
        """Gets location by id"""
        async for location in self.get_locations():
            if location.id == location_id:
                return location

        return None

    async def get_location_by_name(
        self, location_name: str
    ) -> Awaitable[Optional[RWLocation]]:
        """Gets location by name"""
        for location in await self.get_locations():
            if location.name == location_name:
                return location

        return None

    async def search_trips(
        self,
        src_location: RWLocation,
        dest_location: RWLocation,
        date: datetime.datetime,
        adults: int,
        children: int = 0,
    ) -> Awaitable[List[RWTrip]]:
        """Search trips by given critteria"""
        date_str = date.strftime("%Y-%m-%d")

        response = await self._session.search_trips(
            src_location.id,
            dest_location.id,
            date_str,
            adults,
            children,
        )
        response_json = await response.json()
        APIStatusError.raise_for_status(response_json)
        trips = []

        for trip_data in response_json["data"]["trips"]:
            trip = model_mappers.trip_from_json(trip_data)
            trips.append(trip)

        return trips

    async def get_price_summary(
        self, outbound_trip: RWTrip, inbound_trip: Optional[RWTrip] = None
    ) -> Awaitable[RWPriceSummary]:
        """Get price summary for selected trips

        Actually this does not really give you price summary.
        All calculations has to be done manually on the client side.
        This only returns prices for services like how much for an adult or child.
        """

        response = await self._session.get_price_summary(
            outbound_trip.id, inbound_trip.id if inbound_trip is not None else -1
        )
        response_json = await response.json()
        APIStatusError.raise_for_status(response_json)
        return model_mappers.price_summary_from_json(response_json["data"])

    async def get_seats(
        self,
        outbound_trip: RWTrip,
        outbound_wagon: RWWagon,
        adults: int,
        children: int = 0,
        inbound_trip: Optional[RWTrip] = None,
        inbound_wagon: Optional[RWWagon] = None,
    ) -> Awaitable[RWTripSeats]:
        """Get available seats for given wagons/trains"""
        response = await self._session.get_seats(
            outbound_trip.id,
            outbound_wagon.id,
            adults,
            children,
            inbound_trip.id if inbound_trip is not None else -1,
            inbound_wagon.id if inbound_wagon is not None else -1,
        )
        response_json = await response.json()
        APIStatusError.raise_for_status(response_json)
        return model_mappers.seats_from_json(response_json["data"])

    async def book_tickets(
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
    ) -> Awaitable[RWBooking]:
        """Proceed to booking tickets"""

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

        response = await self._session.book_tickets(
            contact_mobile=contact.mobile,
            contact_email=contact.email,
            contact_main_contact=contact.main_contact,
            passengers=[
                {
                    "name": passenger.name,
                    "surname": passenger.surname,
                    "dob": passenger.dob.strftime("%d-%m-%Y"),
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
        response_json = await response.json()
        APIStatusError.raise_for_status(response_json)
        return model_mappers.booking_from_json(response_json["data"]["booking"])
