import pytest
from werkzeug import Client, Response

from tests.data import *


def perform_test_request(client, username=None, password=None) -> Response:
    json = {}
    if username is not None:
        json['username'] = username
    if password is not None:
        json['password'] = password
    return client.post('/api/v1/auth', json=json)


def test_invalid_method(client: Client):
    for method in ["get", "put", "patch", "delete"]:
        response: Response = getattr(client, method)('/api/v1/auth')
        assert response.status_code == 405


def test_incomplete_request(client: Client):
    response = perform_test_request(client)
    assert response.status_code == 400
    response = perform_test_request(client, username='Some Name')
    assert response.status_code == 400
    response = perform_test_request(client, password='Some Pass')
    assert response.status_code == 400


def test_absent_user(client: Client):
    response = perform_test_request(client, username='nonexistent-name', password='Some Password')
    assert response.status_code == 401


@pytest.mark.usefixtures('test_data')
def test_existing_user_invalid_password(client: Client):
    response = perform_test_request(client, username=user1name, password=user1pass + '.')
    assert response.status_code == 401


@pytest.mark.usefixtures('test_data')
def test_valid_auth(client: Client):
    response = perform_test_request(client, username=user1name, password=user1pass)
    assert response.status_code == 200
    # TODO: Validate Access Token


@pytest.mark.usefixtures('test_data')
def test_superfluous_arguments(client: Client):
    response: Response = client.post('/api/v1/auth', json={
        'username': user1name,
        'password': user1pass,
        'extra': 'Some Value'
    })
    assert response.status_code == 200
    # TODO: Validate Access Token
