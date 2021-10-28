from werkzeug import Client, Response


def test_root(client: Client):
    response: Response = client.get('/')
    assert response.status_code == 404
    response = client.get('/api')
    assert response.status_code == 404
    response = client.get('/api/v1')
    assert response.status_code == 404
