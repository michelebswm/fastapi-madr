from sqlalchemy import select

from madr.models import User


def test_create_user_db(session):
    user = User(username='Michele', email='mi@teste.com', senha='12345')
    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == user.email))
    assert result.username == user.username
