from http import HTTPStatus

from madr.utils import sanitization_data
from tests.conftest import LivroFactory


def test_create_livro_ok(client, token):
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


def test_create_livro_conflict(session, client, token):
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
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.delete('/livro/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Livro deletado no MADR'}


def test_delete_livro_not_found(session, client, token):
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.delete('/livro/2', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_patch_livro_ano(session, client, token):
    new_year = 2024
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.patch(
        '/livro/1', headers={'Authorization': f'Bearer {token}'}, json={'ano': new_year}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['ano'] == new_year


def test_patch_livro_titulo(session, client, token):
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.patch(
        '/livro/1', headers={'Authorization': f'Bearer {token}'}, json={'titulo': 'Teste'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['titulo'] == 'teste'


def test_patch_livro_not_found(session, client, token):
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.patch(
        '/livro/2', headers={'Authorization': f'Bearer {token}'}, json={'titulo': 'Teste'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_patch_livro_conflict(session, client, token):
    session.bulk_save_objects(LivroFactory.build_batch(1, titulo='teste'))
    session.commit()
    session.bulk_save_objects(LivroFactory.build_batch(1))
    session.commit()

    response = client.patch(
        '/livro/2', headers={'Authorization': f'Bearer {token}'}, json={'titulo': 'Teste'}
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Livro á consta no MADR'}
