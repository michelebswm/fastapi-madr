from http import HTTPStatus


def test_root_deve_retornar_ok_e_messagem(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Projeto Madr (Meu Acervo Digital de Romances)'}
