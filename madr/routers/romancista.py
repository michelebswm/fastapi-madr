from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Romancista, User
from madr.schemas import RomancistaPublic, RomancistaSchema
from madr.security import get_current_user
from madr.utils import sanitization_data

router = APIRouter(prefix='/romancista', tags=['romancista'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('', status_code=HTTPStatus.CREATED, response_model=RomancistaPublic)
def create_romancista(
    romancista: RomancistaSchema, session: T_Session, current_user: T_CurrentUser
):
    db_romancista = session.scalar(
        select(Romancista).where(Romancista.nome == sanitization_data(romancista.nome))
    )
    if db_romancista:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Romancista já consta no MADR')

    db_romancista = Romancista(nome=sanitization_data(romancista.nome))
    session.add(db_romancista)
    session.commit()
    session.refresh(db_romancista)

    return db_romancista
