import pytest
from django.core.management import call_command
from django.test import Client


# fixture prepopulates database with test objects from test_data.json
@pytest.fixture(scope="session")
def db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "data/test_data.json")


@pytest.fixture
def client():
    client = Client()
    return client
