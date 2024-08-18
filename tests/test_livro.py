from http import HTTPStatus


def test_create_livro_ok(client, token):
    response = client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={'ano': 1974, 'titulo': 'café da manhã dos campeões', 'romancista_id': 1},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'ano': 1974,
        'titulo': 'café da manhã dos campeões',
        'romancista_id': 1,
    }
