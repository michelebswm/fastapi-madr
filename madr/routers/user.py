from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import User
from madr.schemas import Message, UserPublic, UserSchema
from madr.security import get_current_user, get_password_hash

router = APIRouter(prefix='/conta', tags=['conta'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email))
    )

    if db_user:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='conta já consta no MADR')

    db_user = User(username=user.username, email=user.email, senha=get_password_hash(user.senha))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put('/{id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(id: int, user: UserSchema, session: T_Session, current_user: T_CurrentUser):
    if current_user.id != id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Não autorizado')

    current_user.username = user.username
    current_user.email = user.email
    current_user.senha = get_password_hash(user.senha)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(id: int, session: T_Session, current_user: T_CurrentUser):
    if current_user.id != id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Não autorizado')
    session.delete(current_user)
    session.commit()

    return {'message': 'Conta deletada com sucesso'}
