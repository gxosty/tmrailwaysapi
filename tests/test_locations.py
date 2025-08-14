from tmrailwaysapi import RWClient


class TestClientLocations:
    def setup_class(self):
        self.client = RWClient()

    def test_fetch_locations(self):
        assert self.client.locations

    def test_get_location_by_id(self):
        # we know that id 17 is "Aşgabat"
        assert self.client.get_location_by_id(17).name == "Aşgabat"

    def test_get_location_by_name(self):
        assert self.client.get_location_by_name("Aşgabat").id == 17

    def test_get_nonexisting_location_by_id_and_name(self):
        assert self.client.get_location_by_id("Helluwa") is None
        assert self.client.get_location_by_name("Helluwa") is None
