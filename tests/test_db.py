from sqlalchemy import select

from madr.models import Conta


def test_create_conta_db(session):
    conta = Conta(username='Michele', email='mi@teste.com', senha='12345')
    session.add(conta)
    session.commit()

    result = session.scalar(select(Conta).where(Conta.email == conta.email))
    assert result.username == conta.username
