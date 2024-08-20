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
    assert response.json() == {'detail': 'Romancista já consta no MADR'}


def test_delete_romancista_ok(session, client, token):
    session.bulk_save_objects(RomancistaFactory.create_batch(1))
    session.commit()

    response = client.delete('/romancista/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Romancista deletada no MADR'}


def test_delete_romancista_not_found(client, token):
    response = client.delete('/romancista/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_patch_romancista_ok(client, session, token):
    session.bulk_save_objects(RomancistaFactory.create_batch(1, nome='romancista teste'))
    session.commit()

    response = client.patch(
        '/romancista/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Romancista Test'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'nome': 'romancista test'}


def test_patch_romancista_conflict(client, session, token):
    session.bulk_save_objects(RomancistaFactory.create_batch(1, nome='romancista test um'))
    session.commit()
    session.bulk_save_objects(RomancistaFactory.create_batch(1, nome='romancista test dois'))
    session.commit()

    response = client.patch(
        '/romancista/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Romancista Test Dois'},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Romancista já consta no MADR'}


def test_patch_romancista_not_found(client, token):
    response = client.patch(
        '/romancista/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Romancista Test'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_get_romancista_by_id_ok(client, session, token):
    session.bulk_save_objects(RomancistaFactory.create_batch(1, nome='romancista test'))
    session.commit()

    response = client.get('/romancista/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'nome': 'romancista test'}


def test_get_romancista_by_id_not_found(client, token):
    response = client.get('/romancista/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_get_romancista_filter_name_return_5_romancistas(client, token, session):
    expected_romancista = 5
    session.bulk_save_objects(RomancistaFactory.create_batch(5))
    session.commit()

    response = client.get('/romancista?nome=a', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['romancistas']) == expected_romancista


def test_get_romancista_filter_name_return_empty(client, token, session):
    expected_romancista = 0
    response = client.get('/romancista?nome=a', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['romancistas']) == expected_romancista
