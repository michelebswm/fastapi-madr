from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Livro, User
from madr.schemas import LivroPublic, LivroSchema
from madr.security import get_current_user
from madr.utils import sanitization_data

router = APIRouter(prefix='/livro', tags=['livro'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('', status_code=HTTPStatus.CREATED, response_model=LivroPublic)
def create_livro(livro: LivroSchema, session: T_Session, current_user: T_CurrentUser):
    db_livro = session.scalar(select(Livro).where(Livro.titulo == sanitization_data(livro.titulo)))
    if db_livro:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Livro á consta no MADR')

    db_livro = Livro(
        ano=livro.ano, titulo=sanitization_data(livro.titulo), romancista_id=livro.romancista_id
    )
    session.add(db_livro)
    session.commit()
    session.refresh(db_livro)

    return db_livro
