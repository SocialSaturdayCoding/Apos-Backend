import pytest

from apos.extensions import app, db


@pytest.fixture(scope='function')
def client():
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
def init_database(client):
    """
    This fixture sets up the database for testing.
    :param client: The test client (we need to make sure that the client fixture runs first).
    """
    db.create_all()
    # TODO: Maybe insert test data?
    yield db
    db.session.remove()
    db.drop_all()
