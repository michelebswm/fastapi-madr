from http import HTTPStatus

from fastapi import FastAPI

from madr.routers import auth, contas, livro, romancista
from madr.schemas import Message

app = FastAPI()
app.include_router(contas.router)
app.include_router(auth.router)
app.include_router(livro.router)
app.include_router(romancista.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Projeto Madr (Meu Acervo Digital de Romances)'}
