from pydantic import BaseModel
from pydantic.types import EmailStr
from sqlalchemy.sql.sqltypes import UUID


class UserCreate(BaseModel):
    tenant_id: UUID
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    active: bool
