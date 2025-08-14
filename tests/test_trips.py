import datetime

from tmrailwaysapi import RWClient, RWLocation


class TestClientTrips:
    def setup_class(self):
        self.client = RWClient()

    def test_search_trips(self):
        # Search for available trips in next 5 days
        src_location = self.client.get_location_by_name("Aşgabat")
        dest_location = self.client.get_location_by_name("Daşoguz")
        date = datetime.datetime.now() + datetime.timedelta(days=5)

        _ = self.client.search_trips(src_location, dest_location, date, adults=1)

        assert True

    def test_invalid_search_trip_src_location(self):
        src_location = RWLocation(id=2555, name="what")
        dest_location = self.client.get_location_by_name("Daşoguz")
        
        date = datetime.datetime.now() + datetime.timedelta(days=5)

        trips = self.client.search_trips(src_location, dest_location, date, adults=1)

        assert len(trips) == 0
