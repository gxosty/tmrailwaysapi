from typing import Dict, List, Awaitable

import asyncio
import aiohttp

from .session import RWSession


class RWAsyncSession:
    """The async version of RWSession"""

    def __init__(self, hostname: str) -> None:
        self._hostname = hostname

        self._client_session = aiohttp.ClientSession(
            headers=RWSession.get_default_headers(), raise_for_status=True
        )

    async def _close(self) -> Awaitable:
        await self._client_session.close()
        await asyncio.sleep(1)

    async def get(self, path: str = "", *args, **kwargs) -> Awaitable[aiohttp.ClientResponse]:
        return await self._client_session.get(
            "https://" + self._hostname + path, *args, **kwargs
        )

    async def post(self, path: str = "", *args, **kwargs) -> Awaitable[aiohttp.ClientResponse]:
        return await self._client_session.post(
            "https://" + self._hostname + path, *args, **kwargs
        )

    def get_hostname(self) -> str:
        return self._hostname

    async def get_main_page(self) -> Awaitable[aiohttp.ClientResponse]:
        return await self.get()

    async def get_stations(self) -> Awaitable[aiohttp.ClientResponse]:
        return await self.get("/railway-api/stations")

    async def search_trips(
        self,
        src_location: int,
        dest_location: int,
        date: str,
        adults: int,
        children: int = 0,
    ) -> Awaitable[aiohttp.ClientResponse]:
        return await self.post(
            "/railway-api/trips",
            json={
                "source": str(src_location),
                "destination": str(dest_location),
                "date": date,
                "adult": adults,
                "child": children,
            },
        )

    async def get_price_summary(
        self, outbound_trip_id: int, inbound_trip_id: int = -1
    ) -> Awaitable[aiohttp.ClientResponse]:
        if inbound_trip_id == -1:
            return await self.get(f"/railway-api/trips/{outbound_trip_id}/price_summary?")

        return await self.get(
            "/railway-api/roundtrips"
            f"/outbound/{outbound_trip_id}/inbound/{inbound_trip_id}/price_summary?"
        )

    async def get_seats(
        self,
        outbound_trip_id: int,
        outbound_wagon_id: int,
        adults: int,
        children: int,
        inbound_trip_id: int = -1,
        inbound_wagon_id: int = -1,
    ) -> Awaitable[aiohttp.ClientResponse]:
        if inbound_trip_id == -1:
            return await self.post(
                f"/railway-api/trips/{outbound_trip_id}",
                json={
                    "adult": adults,
                    "child": children,
                    "outbound_wagon_type_id": outbound_wagon_id,
                },
            )

        return await self.post(
            "/railway-api/roundtrips"
            f"/outbound/{outbound_trip_id}/inbound/{inbound_trip_id}",
            json={
                "adult": adults,
                "child": children,
                "outbound_wagon_type_id": outbound_wagon_id,
                "inbound_wagon_type_id": inbound_wagon_id,
            },
        )

    async def book_tickets(
        self,
        contact_mobile: str,
        contact_email: str,
        contact_main_contact: str,
        passengers: List[Dict[str, str]],
        outbound_journey_id: int,
        outbound_wagon_id: int,
        outbound_seat_id: int,
        api_client: str = "web",
        has_media_wifi: bool = False,
        has_lunchbox: bool = False,
        bedding_type: str = "default",
        inbound_journey_id: int = -1,
        inbound_wagon_id: int = -1,
        inbound_seat_id: int = -1,
    ) -> Awaitable[aiohttp.ClientResponse]:
        if (
            inbound_journey_id != -1
            and inbound_wagon_id != -1
            and inbound_seat_id != -1
        ):
            inbound = {
                "selected_journeys": [
                    {
                        "id": inbound_journey_id,
                        "seats": [
                            {
                                "id": inbound_seat_id,
                                "train_wagon_id": inbound_wagon_id,
                            },
                        ],
                    },
                ],
            }
        else:
            inbound = None

        json_data = {
            "has_media_wifi": has_media_wifi,
            "has_lunchbox": has_lunchbox,
            "bedding_type": bedding_type,
            "api_client": api_client,
            "contact": {
                "mobile": contact_mobile,
                "email": contact_email,
                "main_contact": contact_main_contact,
            },
            "passengers": passengers,
            "outbound": {
                "selected_journeys": [
                    {
                        "id": outbound_journey_id,
                        "seats": [
                            {
                                "id": outbound_seat_id,
                                "train_wagon_id": outbound_wagon_id,
                            },
                        ],
                    },
                ],
            },
            "inbound": inbound,
        }

        return await self.post("/railway-api/bookings", json=json_data)
