# where dependensy happen
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.sessions import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# yield provides database session to route, keep it open during request
# finally ensures sessions always closes even if an error occurs 