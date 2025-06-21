from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from bookstore.bookmgmt import router as book_router
from bookstore.database import UserCredentials, get_db
from bookstore.utils import create_access_token  # assuming utils.py is inside bookstore/

app = FastAPI()

app.include_router(book_router, tags=["Books"])


@app.get("/health")
async def get_health():
    return {"status": "up"}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/signup")
async def create_user_signup(user_credentials: UserCredentials, db: Session = Depends(get_db)):
    user = db.query(UserCredentials).filter(UserCredentials.email == user_credentials.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user_credentials.password)
    user_credentials.password = hashed_password
    db.add(user_credentials)
    db.commit()
    db.refresh(user_credentials)
    return {"message": "User created successfully"}


@app.post("/login")
async def login_for_access_token(user_credentials: UserCredentials, db: Session = Depends(get_db)):
    user = db.query(UserCredentials).filter(UserCredentials.email == user_credentials.email).first()
    if not user or not pwd_context.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
