import pytest
from flask_sqlalchemy import SQLAlchemy
from werkzeug import Client

from apos.app import app, db
from tests.data import import_data


@pytest.fixture(scope='function')
def client() -> Client:
    """
    The test client used to send test requests to the APOS backend app.
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    context = app.app_context()
    context.push()
    yield app.test_client()
    context.pop()


@pytest.fixture(scope='function', autouse=True)
def database(client) -> SQLAlchemy:
    """
    This fixture sets up the database for testing.
    :param client: The test client (we need to make sure that the client fixture runs first).
    """
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='function')
def test_data(client, database):
    import_data(database.session)
