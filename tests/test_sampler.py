from faker_locality.sampler import get_location, get_city


def test_get_location():
    location = get_location(country="Pakistan", province="Sindh")
    assert isinstance(location, dict)
    assert "city" in location
    assert location["country"] == "Pakistan"
    assert location["province"] == "Sindh"


def test_get_city():
    city = get_city(country="Pakistan", province="Sindh")
    assert isinstance(city, str)
