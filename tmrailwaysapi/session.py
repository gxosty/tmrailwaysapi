from typing import Dict, List, Any

import requests


class RWSession(requests.Session):
    def __init__(self, *args, hostname: str, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._hostname = hostname

        self.headers.update(RWSession.get_default_headers())

    @staticmethod
    def get_default_headers() -> Dict[str, str]:
        """Get default browser headers"""
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US;en;q=0.9,tk;q=0.8",
            "Cache-Control": "max-age=0",
            "Dnt": "1",
            "Sec-Ch-Ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecute-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        }

        return headers

    # override
    def get(self, path: str = "", *args, **kwargs) -> requests.Response:
        response = super().get("https://" + self._hostname + path, *args, **kwargs)
        response.raise_for_status()
        return response

    # override
    def post(self, path: str = "", *args, **kwargs) -> requests.Response:
        response = super().post("https://" + self._hostname + path, *args, **kwargs)
        response.raise_for_status()
        return response

    def get_hostname(self) -> str:
        return self._hostname

    def get_main_page(self) -> requests.Response:
        return self.get()

    def get_stations(self) -> requests.Response:
        return self.get("/railway-api/stations")

    def search_trips(
        self,
        src_location: int,
        dest_location: int,
        date: str,
        adults: int,
        children: int = 0,
    ) -> requests.Response:
        return self.post(
            "/railway-api/trips",
            json={
                "source": str(src_location),
                "destination": str(dest_location),
                "date": date,
                "adult": adults,
                "child": children,
            },
        )

    def get_price_summary(
        self, outbound_trip_id: int, inbound_trip_id: int = -1
    ) -> requests.Response:
        if inbound_trip_id == -1:
            return self.get(f"/railway-api/trips/{outbound_trip_id}/price_summary?")

        return self.get(
            "/railway-api/roundtrips"
            f"/outbound/{outbound_trip_id}/inbound/{inbound_trip_id}/price_summary?"
        )

    def get_seats(
        self,
        outbound_trip_id: int,
        outbound_wagon_id: int,
        adults: int,
        children: int,
        inbound_trip_id: int = -1,
        inbound_wagon_id: int = -1,
    ) -> requests.Response:
        if inbound_trip_id == -1:
            return self.post(
                f"/railway-api/trips/{outbound_trip_id}",
                json={
                    "adult": adults,
                    "child": children,
                    "outbound_wagon_type_id": outbound_wagon_id,
                },
            )

        return self.post(
            "/railway-api/roundtrips"
            f"/outbound/{outbound_trip_id}/inbound/{inbound_trip_id}",
            json={
                "adult": adults,
                "child": children,
                "outbound_wagon_type_id": outbound_wagon_id,
                "inbound_wagon_type_id": inbound_wagon_id,
            },
        )

    def book_tickets(
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
    ) -> requests.Response:
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

        return self.post("/railway-api/bookings", json=json_data)
