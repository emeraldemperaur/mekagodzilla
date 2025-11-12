# API Helper Functions
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from dotenv import load_dotenv
from mercurius.http_models import Token
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import anyio
import os
import datetime as dt


load_dotenv(verbose=True)
SECRET_KEY = os.getenv("SECRET_KEY", "la-li-li-lu-le-lo")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./iliad.db")

engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False,
                                  expire_on_commit=False, class_=AsyncSession)
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return await anyio.to_thread.run_sync(password_context.verify, plain_password, hashed_password)


async def get_password_hash(password: str) -> str:
    return await anyio.to_thread.run_sync(password_context.hash, password)


def _create_token(*, subject: str, token_type: str, expires_delta: dt.timedelta) -> str:
    now = dt.datetime.now(dt.UTC)
    expire = now + expires_delta
    payload = {"sub": subject, "type": token_type, "exp": int(expire.timestamp())}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_token_pair(user_id: int) -> Token:
    access = _create_token(subject=str(user_id), token_type="access",
                           expires_delta=dt.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh = _create_token(subject=str(user_id), token_type="refresh",
                            expires_delta=dt.timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS))
    return Token(access_token=access, refresh_token=refresh, expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
