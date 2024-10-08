from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Livro, Romancista, User
from madr.schemas import LivroList, LivroPublic, LivroSchema, LivroUpdate, Message
from madr.security import get_current_user
from madr.utils import sanitization_data

router = APIRouter(prefix='/livro', tags=['livro'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('', status_code=HTTPStatus.CREATED, response_model=LivroPublic)
def create_livro(livro: LivroSchema, session: T_Session, current_user: T_CurrentUser):
    db_livro = session.scalar(select(Livro).where(Livro.titulo == sanitization_data(livro.titulo)))
    db_romancista = session.scalar(select(Romancista).where(Romancista.id == livro.romancista_id))

    if db_livro:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Livro á consta no MADR')

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Romancista não consta no MADR'
        )

    db_livro = Livro(
        ano=livro.ano, titulo=sanitization_data(livro.titulo), romancista_id=livro.romancista_id
    )
    session.add(db_livro)
    session.commit()
    session.refresh(db_livro)

    return db_livro


@router.delete('/{id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_livro(id: int, session: T_Session, current_user: T_CurrentUser):
    db_livro = session.scalar(select(Livro).where(Livro.id == id))

    if not db_livro:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR')

    session.delete(db_livro)
    session.commit()

    return {'message': 'Livro deletado no MADR'}


@router.patch('/{id}', response_model=LivroPublic)
def patch_livro(id: int, session: T_Session, current_user: T_CurrentUser, livro: LivroUpdate):
    db_livro = session.scalar(select(Livro).where(Livro.id == id))

    if not db_livro:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR')

    for key, value in livro.model_dump(exclude_unset=True).items():
        if key == 'titulo':
            value_sanitized = sanitization_data(value)
            db_livro_patch = session.scalar(select(Livro).where(Livro.titulo == value_sanitized))
            if db_livro_patch:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT, detail='Livro á consta no MADR'
                )
            setattr(db_livro, key, value_sanitized)
        elif key == 'romancista_id':
            db_romancista = session.scalar(
                select(Romancista).where(Romancista.id == livro.romancista_id)
            )
            if not db_romancista:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail='Romancista não consta no MADR'
                )
            setattr(db_livro, key, value)
        else:
            setattr(db_livro, key, value)

    session.add(db_livro)
    session.commit()
    session.refresh(db_livro)

    return db_livro


@router.get('/{id}', status_code=HTTPStatus.OK, response_model=LivroPublic)
def find_livro(id: int, session: T_Session, current_user: T_CurrentUser):
    db_livro = session.scalar(select(Livro).where(Livro.id == id))
    if not db_livro:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR')

    return db_livro


@router.get('', status_code=HTTPStatus.OK, response_model=LivroList)
def list_livros(  # noqa
    session: T_Session,
    current_user: T_CurrentUser,
    ano: int | None = None,
    titulo: str | None = None,
    offset: int | None = None,
    limit: int | None = 20,
):
    query = select(Livro)

    if ano:
        query = query.where(Livro.ano == ano)

    if titulo:
        query = query.where(Livro.titulo.contains(titulo))

    livros = session.scalars(query.offset(offset).limit(limit)).all()

    return {'livros': livros}
