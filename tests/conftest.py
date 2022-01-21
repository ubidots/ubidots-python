import pytest
import responses

from faker.providers import company, internet, lorem


@pytest.fixture(autouse=True)
def faker_providers(faker):
    faker.add_provider(company)
    faker.add_provider(internet)
    faker.add_provider(lorem)


@pytest.fixture()
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps
