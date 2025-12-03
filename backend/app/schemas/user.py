from pydantic import BaseModel

# For returning user info
class UserRead(BaseModel):
    id: int
    uid: str
    role: str

    class Config:
        orm_mode = True

# For creating/updating users
class UserCreate(BaseModel):
    uid: str
    role: str
    # add password or other fields if required

    class Config:
        orm_mode = True
