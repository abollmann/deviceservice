import pytest

from deviceservice import app

BASE_PATH = '/api/devices'


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_base_path(client):
    pass
