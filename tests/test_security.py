from jwt import decode

from madr.security import create_access_token
from madr.settings import Settings


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data=data)

    result = decode(token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']
