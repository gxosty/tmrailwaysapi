from tmrailwaysapi import RWClient


def test_locations():
    client = RWClient()
    assert client.src_locations
    assert client.dest_locations

