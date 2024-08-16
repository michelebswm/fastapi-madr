from http import HTTPStatus


def test_create_conta_ok(client):
    response = client.post(
        '/conta', json={'username': 'testusername', 'email': 'testemail@test.com', 'senha': '12345'}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'username': 'testusername', 'email': 'testemail@test.com', 'id': 1}


def test_create_conta_conflict_username(client, user):
    response = client.post(
        '/conta', json={'username': user.username, 'email': 'test@test.com', 'senha': '12345'}
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_create_conta_conflict_email(client, user):
    response = client.post(
        '/conta', json={'username': 'testeusername', 'email': user.email, 'senha': '12345'}
    )
    assert response.status_code == HTTPStatus.CONFLICT
