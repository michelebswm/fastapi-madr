from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Conta
from madr.schemas import ContaPublic, ContaSchema

router = APIRouter(prefix='/conta', tags=['conta'])
T_Session = Annotated[Session, Depends(get_session)]


@router.post('', status_code=HTTPStatus.CREATED, response_model=ContaPublic)
def create_conta(conta: ContaSchema, session: T_Session):
    db_conta = session.scalar(
        select(Conta).where((Conta.username == conta.username) | (Conta.email == conta.email))
    )

    if db_conta:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='conta já consta no MADR')

    db_conta = Conta(username=conta.username, email=conta.email, senha=conta.senha)
    session.add(db_conta)
    session.commit()
    session.refresh(db_conta)

    return db_conta
