from http import HTTPStatus


def test_create_user_ok(client):
    response = client.post(
        '/conta', json={'username': 'testusername', 'email': 'testemail@test.com', 'senha': '12345'}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'username': 'testusername', 'email': 'testemail@test.com', 'id': 1}


def test_create_user_conflict_username(client, user):
    response = client.post(
        '/conta', json={'username': user.username, 'email': 'test@test.com', 'senha': '12345'}
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_create_user_conflict_email(client, user):
    response = client.post(
        '/conta', json={'username': 'testeusername', 'email': user.email, 'senha': '12345'}
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_put_user_ok(client, user, token):
    response = client.put(
        f'/conta/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'newusername', 'email': 'newemail@test.com', 'senha': '1234'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'newusername',
        'email': 'newemail@test.com',
        'id': user.id,
    }


def test_put_user_unauthorized(client, token, user):
    response = client.put(
        f'/conta/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'newusername', 'email': 'newemail@test.com', 'senha': '1234'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}


def test_delete_user_ok(client, token, user):
    response = client.delete(f'/conta/{user.id}', headers={'Authorization': f'Bearer {token}'})

    response.status_code == HTTPStatus.OK
    response.json() == {'message': 'Conta deletada com sucesso'}


def test_delete_user_unauthorized(client, token, user):
    response = client.delete(f'/conta/{user.id + 1}', headers={'Authorization': f'Bearer {token}'})

    response.status_code == HTTPStatus.UNAUTHORIZED
