from http import HTTPStatus

from jwt import decode

from madr.security import create_access_token
from madr.settings import Settings


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data=data)

    result = decode(token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid_token(client, user, token):
    response = client.delete(
        f'/conta/{user.id}', headers={'Authorization': 'Bearer tokeN-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
