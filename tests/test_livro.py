from http import HTTPStatus

from madr.utils import sanitization_data
from tests.conftest import LivroFactory


def test_create_livro_ok(client, token):
    response = client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={'ano': 1974, 'titulo': 'Café da manhã dos campeões', 'romancista_id': 1},
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
        json={'ano': 1974, 'titulo': 'Androides Sonham Com Ovelhas Elétricas?', 'romancista_id': 1},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Livro á consta no MADR'}
