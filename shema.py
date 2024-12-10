from pydantic import BaseModel, field_validator


class BaseAdv(BaseModel):
    heading: str


class BaseUser(BaseModel):
    name: str


class CreatAdv(BaseAdv):
    heading: str
    description: str
    creator: str


class UpdateAdv(BaseAdv):
    heading: str | None = None
    description: str | None = None
    creator: str | None = None


class CreatUser(BaseUser):
    name: str
    password: str
    email: str


class UpdateUser(BaseUser):
    name: str | None = None
    password: str | None = None
    email: str | None = None