from uuid import UUID, uuid4

from pydantic import BaseModel


class AddressModel(BaseModel):
    street: str
    city: str
    state: str
    zip: str


class UserModel(BaseModel):
    first_name: str
    last_name: str


class ChildModel(UserModel):
    id: str


class ParentModel(UserModel, AddressModel):
    id: str
    child: ChildModel


