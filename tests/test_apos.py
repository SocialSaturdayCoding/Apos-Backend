from werkzeug.test import Client
from werkzeug.wrappers import Response


def test_root(client: Client):
    rv: Response = client.get('/')
    assert rv.status_code == 404
