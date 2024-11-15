from pydantic import BaseModel





class UserSchema(BaseModel):
    id: int
    username: str


class UserInDB(BaseModel):
    username: str
    hashed_password: str


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(UserRegister):
    pass

