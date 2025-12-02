from pydantic import BaseModel

class UserRead(BaseModel):
    id: int
    uid: str
    role: str

    class Config:
        orm_mode = True
