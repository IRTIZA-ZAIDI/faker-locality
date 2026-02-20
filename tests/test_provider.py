from faker import Faker
from faker_locality.provider import Provider


def test_real_city():
    fake = Faker()
    fake.add_provider(Provider)

    # Test city sampling
    city = fake.real_city(country="Pakistan", province="Sindh")
    assert isinstance(city, str)
    assert city  # Ensure the city name is not empty


def test_real_location():
    fake = Faker()
    fake.add_provider(Provider)

    # Test location sampling
    location = fake.real_location(country="Pakistan", province="Sindh")
    assert isinstance(location, dict)
    assert "city" in location
    assert "province" in location
    assert "country" in location
