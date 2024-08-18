from http import HTTPStatus


def test_create_romancista_ok(client, token):
    response = client.post(
        '/romancista',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Romancista Teste'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'nome': 'Romancista Teste'}
