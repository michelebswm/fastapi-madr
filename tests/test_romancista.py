from http import HTTPStatus

from tests.conftest import RomancistaFactory


def test_create_romancista_ok(client, token):
    response = client.post(
        '/romancista',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Romancista Teste'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'nome': 'romancista teste'}


def test_create_romancista_conflict(client, session, token):
    session.bulk_save_objects(RomancistaFactory.create_batch(1, nome='romancista teste'))
    session.commit()

    response = client.post(
        '/romancista',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Romancista Teste'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
