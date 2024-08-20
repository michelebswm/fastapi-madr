from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Romancista, User
from madr.schemas import (
    Message,
    RomancistaList,
    RomancistaPublic,
    RomancistaSchema,
    RomancistaUpdate,
)
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


@router.delete('/{id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_romancista(id: int, session: T_Session, current_user: T_CurrentUser):
    db_romancista = session.scalar(select(Romancista).where(Romancista.id == id))
    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Romancista não consta no MADR'
        )

    session.delete(db_romancista)
    session.commit()

    return {'message': 'Romancista deletada no MADR'}


@router.patch('/{id}', status_code=HTTPStatus.OK, response_model=RomancistaPublic)
def patch_romancista(
    id: int, session: T_Session, current_user: T_CurrentUser, romancista: RomancistaUpdate
):
    db_romancista = session.scalar(select(Romancista).where(Romancista.id == id))
    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Romancista não consta no MADR'
        )

    for key, value in romancista.model_dump(exclude_unset=True).items():
        if key == 'nome':
            value_sanitized = sanitization_data(value)
            db_romancista_patch = session.scalar(
                select(Romancista).where(Romancista.nome == value_sanitized)
            )
            if db_romancista_patch:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT, detail='Romancista já consta no MADR'
                )
            setattr(db_romancista, key, value_sanitized)
        else:  # pragma: no cover
            setattr(db_romancista, key, value)

    session.add(db_romancista)
    session.commit()
    session.refresh(db_romancista)

    return db_romancista


@router.get(
    '/{id}',
    summary='Busca romancista por id',
    status_code=HTTPStatus.OK,
    response_model=RomancistaPublic,
)
def get_romancista_by_id(id: int, session: T_Session, current_user: T_CurrentUser):
    db_romancista = session.scalar(select(Romancista).where(Romancista.id == id))
    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Romancista não consta no MADR'
        )

    return db_romancista


@router.get('', status_code=HTTPStatus.OK, response_model=RomancistaList)
def list_romancista(  # noqa
    session: T_Session,
    current_user: T_CurrentUser,
    nome: str | None = None,
    offset: int | None = None,
    limit: int | None = 20,
):
    query = select(Romancista)

    if nome:
        query = query.where(Romancista.nome.contains(nome))

    romancistas = session.scalars(query.offset(offset).limit(limit)).all()

    return {'romancistas': romancistas}
