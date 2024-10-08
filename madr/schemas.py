from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    senha: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class LivroSchema(BaseModel):
    ano: int
    titulo: str
    romancista_id: int


class LivroPublic(LivroSchema):
    id: int


class LivroUpdate(BaseModel):
    ano: int | None = None
    titulo: str | None = None
    romancista_id: int | None = None


class LivroList(BaseModel):
    livros: list[LivroPublic]


class RomancistaSchema(BaseModel):
    nome: str


class RomancistaPublic(RomancistaSchema):
    id: int


class RomancistaUpdate(BaseModel):
    nome: str | None = None


class RomancistaList(BaseModel):
    romancistas: list[RomancistaPublic]
