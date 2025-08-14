from typing import Dict, Optional

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
        babies: int = 0,
        two_way: bool = False,
        return_date: Optional[str] = None,
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
