from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Conta
from madr.schemas import ContaPublic, ContaSchema, Message
from madr.security import get_current_user, get_password_hash

router = APIRouter(prefix='/conta', tags=['conta'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Conta, Depends(get_current_user)]


@router.post('', status_code=HTTPStatus.CREATED, response_model=ContaPublic)
def create_conta(conta: ContaSchema, session: T_Session):
    db_conta = session.scalar(
        select(Conta).where((Conta.username == conta.username) | (Conta.email == conta.email))
    )

    if db_conta:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='conta já consta no MADR')

    db_conta = Conta(
        username=conta.username, email=conta.email, senha=get_password_hash(conta.senha)
    )
    session.add(db_conta)
    session.commit()
    session.refresh(db_conta)

    return db_conta


@router.put('/{id}', status_code=HTTPStatus.OK, response_model=ContaPublic)
def update_conta(id: int, conta: ContaSchema, session: T_Session, current_user: T_CurrentUser):
    if current_user.id != id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Não autorizado')

    current_user.username = conta.username
    current_user.email = conta.email
    current_user.senha = get_password_hash(conta.senha)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_conta(id: int, session: T_Session, current_user: T_CurrentUser):
    if current_user.id != id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Não autorizado')
    session.delete(current_user)
    session.commit()

    return {'message': 'Conta deletada com sucesso'}
