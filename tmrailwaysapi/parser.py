from typing import List

from bs4 import BeautifulSoup as BS

from .models import RWLocation


class RWParser:
    """Content parser for parsing out information"""

    @staticmethod
    def parse_locations(html_content: str) -> (List[RWLocation], List[RWLocation]):
        soup = BS(html_content, "lxml")
        one_way = soup.find(id="one_way")
        two_way = soup.find(id="two_way")
        one_way_options = one_way.find_all("option")
        two_way_options = two_way.find_all("option")
        src_locations = []
        dest_locations = []

        for option in one_way_options:
            location = RWLocation(id=option.get("value"), name=option.text.strip())

            src_locations.append(location)

        for option in two_way_options:
            location = RWLocation(id=option.get("value"), name=option.text.strip())

            dest_locations.append(location)

        return src_locations, dest_locations
