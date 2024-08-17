from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class ContaSchema(BaseModel):
    username: str
    email: EmailStr
    senha: str


class ContaPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
