from http import HTTPStatus

from madr.utils import sanitization_data
from tests.conftest import LivroFactory, RomancistaFactory


def test_create_livro_ok(client, token, session):
    session.bulk_save_objects(RomancistaFactory.build_batch(1))
    session.commit()

    response = client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'ano': 1974,
            'titulo': sanitization_data('Café da manhã dos campeões'),
            'romancista_id': 1,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'ano': 1974,
        'titulo': 'café da manhã dos campeões',
        'romancista_id': 1,
    }


def test_create_livro_romancista_not_found(client, token):
    response = client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'ano': 1974,
            'titulo': sanitization_data('Café da manhã dos campeões'),
            'romancista_id': 1,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_create_livro_conflict(session, client, token):
    session.bulk_save_objects(RomancistaFactory.build_batch(1))
    session.bulk_save_objects(
        LivroFactory.build_batch(
            1, titulo=sanitization_data('Androides Sonham Com Ovelhas Elétricas?')
        )
    )
    session.commit()

    response = client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'ano': 1974,
            'titulo': sanitization_data('Androides Sonham Com Ovelhas Elétricas?'),
            'romancista_id': 1,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Livro á consta no MADR'}


def test_delete_livro_ok(session, client, token):
    session.bulk_save_objects(RomancistaFactory.build_batch(1))
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.delete('/livro/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Livro deletado no MADR'}


def test_delete_livro_not_found(client, token):
    response = client.delete('/livro/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_patch_livro_ano(session, client, token):
    new_year = 2024
    session.bulk_save_objects(RomancistaFactory.build_batch(1))
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.patch(
        '/livro/1', headers={'Authorization': f'Bearer {token}'}, json={'ano': new_year}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['ano'] == new_year


def test_patch_livro_titulo(session, client, token):
    session.bulk_save_objects(RomancistaFactory.build_batch(1))
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.patch(
        '/livro/1', headers={'Authorization': f'Bearer {token}'}, json={'titulo': 'Teste'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['titulo'] == 'teste'


def test_patch_livro_romancista_id(session, client, token):
    new_romancista = 2
    session.bulk_save_objects(RomancistaFactory.build_batch(2))
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.patch(
        '/livro/1', headers={'Authorization': f'Bearer {token}'}, json={'romancista_id': 2}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['romancista_id'] == new_romancista


def test_patch_livro_not_found(session, client, token):
    session.bulk_save_objects(RomancistaFactory.build_batch(1))
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.patch(
        '/livro/2', headers={'Authorization': f'Bearer {token}'}, json={'titulo': 'Teste'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_patch_livro_romancista_not_found(session, client, token):
    session.bulk_save_objects(RomancistaFactory.build_batch(1))
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.patch(
        '/livro/1', headers={'Authorization': f'Bearer {token}'}, json={'romancista_id': 2}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_patch_livro_conflict(session, client, token):
    session.bulk_save_objects(RomancistaFactory.build_batch(1))
    session.bulk_save_objects(LivroFactory.build_batch(1, titulo='teste'))
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.patch(
        '/livro/2', headers={'Authorization': f'Bearer {token}'}, json={'titulo': 'Teste'}
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Livro á consta no MADR'}


def test_get_livro_by_id_ok(session, client, token):
    session.bulk_save_objects(RomancistaFactory.build_batch(1))
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.get('/livro/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK


def test_get_livro_by_id_not_found(session, client, token):
    session.bulk_save_objects(RomancistaFactory.build_batch(1))
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.get('/livro/2', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_list_livro_filter_ano_return_5(session, client, token):
    expected_livros = 5
    session.bulk_save_objects(RomancistaFactory.build_batch(1))
    session.bulk_save_objects(LivroFactory.build_batch(5, ano=2024))
    session.commit()

    response = client.get('/livro?ano=2024', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['livros']) == expected_livros


def test_list_livro_filter_titulo_return_5(session, client, token):
    expected_livros = 5
    session.bulk_save_objects(RomancistaFactory.build_batch(1))
    session.bulk_save_objects(LivroFactory.build_batch(5))
    session.commit()

    response = client.get('/livro?titulo=a', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['livros']) == expected_livros


def test_list_livro_filter_combined_return_5(session, client, token):
    expected_livros = 5
    session.bulk_save_objects(RomancistaFactory.build_batch(1))
    session.bulk_save_objects(LivroFactory.build_batch(5, ano=2024))
    session.commit()

    response = client.get('/livro?ano=2024&titulo=a', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['livros']) == expected_livros


def test_list_livro_return_empty(client, token):
    expected_livros = 0
    response = client.get('/livro?ano=2024', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['livros']) == expected_livros
