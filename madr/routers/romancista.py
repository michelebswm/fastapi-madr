from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Conta, Romancista
from madr.schemas import RomancistaPublic, RomancistaSchema
from madr.security import get_current_user

router = APIRouter(prefix='/romancista', tags=['romancista'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Conta, Depends(get_current_user)]


@router.post('', status_code=HTTPStatus.CREATED, response_model=RomancistaPublic)
def create_romancista(
    romancista: RomancistaSchema, session: T_Session, current_user: T_CurrentUser
):
    db_romancista = Romancista(nome=romancista.nome)
    session.add(db_romancista)
    session.commit()
    session.refresh(db_romancista)

    return db_romancista
