from werkzeug import Client, Response


def test_get_empty(client: Client):
    response: Response = client.get('/api/v1/coupons')
    assert response.status_code == 200
    assert response.get_json() == []
