from http import HTTPStatus


def test_create_conta_ok(client):
    response = client.post(
        '/conta', json={'username': 'test', 'email': 'test@test.com', 'senha': '12345'}
    )
    assert response.status_code == HTTPStatus.CREATED
