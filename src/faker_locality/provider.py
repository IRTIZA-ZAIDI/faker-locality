from typing import Optional
from faker.providers import BaseProvider
from faker_locality.sampler import get_location, get_city


class Provider(BaseProvider):
    def real_city(
        self, country: Optional[str] = None, province: Optional[str] = None
    ) -> str:
        """Return a real city based on the country/province."""
        return get_city(country=country, province=province)

    def real_location(
        self, country: Optional[str] = None, province: Optional[str] = None
    ) -> dict:
        """Return a real location (city, province, country) based on the input."""
        return get_location(country=country, province=province)
