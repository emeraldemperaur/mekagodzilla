# FastAPI (Concurrent) API Server
from __future__ import annotations

import asyncio
import multiprocessing
from typing import cast
from artificer import ASCI_BLUE, ASCI_ARROW, ASCI_RESET, ASCI_TEAL, ASCI_MERCURY, ASCI_GREEN, ASCI_POWER
import datetime as dt
import os
import time
from collections import deque
from typing import Annotated, Optional, Set, AsyncGenerator
import anyio
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy import ForeignKey, String, Text, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column, joinedload
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from artisan import Artisan
from heimdall import Heimdall

#load environment variables from .env file
load_dotenv(verbose=True)
SECRET_KEY = os.getenv("SECRET_KEY", "la-li-li-lu-le-lo")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./iliad.db")
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
RATE_LIMIT_PER_MIN = int(os.getenv("RATE_LIMIT_PER_MIN", 120))
USER_DEFAULT_ROLE = os.getenv("USER_DEFAULT_ROLE", "admin")
ROOT_ADMIN_DEFAULT_ROLE = os.getenv("ROOT_ADMIN_DEFAULT_ROLE", "root")
DEV_MODE = os.getenv("DEV_MODE", "false").lower() in {"yes","true", "1", "on"}
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 4134))

engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False,
                                  expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

heimall_object = None

class Mercurius:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(Mercurius, cls).__new__(cls)
        return cls._instance  # Always return the existing instance
    def __init__(self, version, environment):
        if not hasattr(self, '_initialized'):
            self.app_server = FastAPI(title="Mercurius", description="MekaGodzilla RPA Server API")
            self.version = version
            self.environment = environment
            self.config = uvicorn.Config(self.app_server,
                                         host=os.getenv("HOST", "127.0.0.1"),
                                         port=int(os.getenv("PORT", 4134)),
                                         log_level="info",
                                         workers=Mercurius.recommended_workers(Mercurius.detect_cpu_cores()))
            self.server_app = uvicorn.Server(self.config)
            self._initialized = True

    def start_server(self):
        if self._initialized:
            load_dotenv()
            print(F"{ASCI_GREEN}{ASCI_MERCURY} Mercurius Activated {ASCI_RESET}")
            print(F"\t{ASCI_TEAL}{ASCI_POWER} API Server Online :: "
                  F"{Mercurius.detect_cpu_cores()} CPU Cores {ASCI_RESET}")
            asyncio.run(self.server_app.serve())

    @staticmethod
    def init_log():
        print(F"{ASCI_BLUE}{ASCI_ARROW} Mercurius Initialized{ASCI_RESET}")

    @staticmethod
    def detect_cpu_cores() -> int:
        try:
            return len(os.sched_getaffinity(0))
        except Exception:
            return multiprocessing.cpu_count()

    @staticmethod
    def recommended_workers(cores: int) -> int:
        return max(1, min(8, cores * 2 + 1))

# Database Models


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[EmailStr] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(4096), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="admin", nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now(dt.timezone.utc), nullable=False)
    artifacts: Mapped[list["Artifact"]] = relationship("Artifact", back_populates="owner", cascade="all, delete-orphan")


class Artifact(Base):
    __tablename__ = "artifacts"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), unique=False, index=True, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now(dt.UTC), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    owner: Mapped[User] = relationship("User", back_populates="artifacts")


heimdall = Heimdall("MekaGodzilla", F"{os.getenv("ENVIRONMENT", "development")}")
mercurius = Mercurius("MekaGodzilla", F"{os.getenv("ENVIRONMENT", "development")}")

@mercurius.app_server.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# CORS Middleware
mercurius.app_server.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rate Limiter Middleware
class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit_per_min: int = 120, window_sec: int = 60):
        super().__init__(app)
        self.limit = limit_per_min
        self.window = float(window_sec)
        self.buckets:  dict[str, deque[float]] = {}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = time.monotonic()
        dq = self.buckets.setdefault(client_ip, deque())
        while dq and now - dq[0] > self.window:
            dq.popleft()
        if len(dq) >= self.limit:
            return Response("WTF! Too Many HTTP Requests", 429)
        dq.append(now)
        return await call_next(request)


mercurius.app_server.add_middleware(RateLimiterMiddleware, limit_per_min=RATE_LIMIT_PER_MIN)

# Schemas


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    platform: str = F"{Artisan.get_platform()}"


class TokenRefrehIn(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str
    type: str
    exp: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: dt.datetime


class ArtifactCreate(BaseModel):
    title: str
    type: str
    content: str


class ArtifactOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    type: str
    created_at: dt.datetime
    owner_id: int
    owner: UserOut
    content: Optional[str]

# Helpers


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
DB = Annotated[AsyncSession, Depends(get_db)]


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

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DB) -> type[User] | None:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Unauthorized. Couldn't validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        data = TokenPayload(**payload)
        if data.type != "access":
            raise credentials_exception
        user_id = int(data.sub)
    except (JWTError, ValueError):
        raise credentials_exception

    user = await db.get(User, user_id)
    if not user or not user.is_active:
        raise credentials_exception
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

def require_roles(*allowed: str):
    allowed_set: Set[str] = {r.lower() for r in allowed}
    async def _dep(current_user: CurrentUser) -> User:
        if current_user.role not in allowed_set:
            raise HTTPException(status_code=403, detail=F"Forbidden: Not allowed for this user ({current_user.role})")
        return current_user
    return _dep


# API Endpoints
## API Authentication Routes
@mercurius.app_server.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: DB):
    role = (user_in.role or USER_DEFAULT_ROLE).lower()
    user = User(email=user_in.email, hashed_password=await get_password_hash(password=user_in.password), role=role)
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail=F"User {user_in.email} already exists")
    await db.refresh(user)
    heimdall.info_log(F"Mercurius API Server :: HTTP POST::({user.email}) "
                      F"User Register")
    return user

@mercurius.app_server.post("/auth/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DB):
    sql_statement = select(User).where(User.email == form_data.username)
    result = await db.execute(sql_statement)
    user = result.scalar_one_or_none()
    if not user or not await verify_password(form_data.password, cast(str, cast(object, user.hashed_password))):
        raise HTTPException(status_code=400, detail=F"Invalid username or password")
    heimdall.info_log(F"Mercurius API Server :: HTTP POST::({user.email}) "
                      F"User Log In")
    return create_token_pair(cast(int, cast(object, user.id)))

@mercurius.app_server.post("/auth/refresh", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh_tokens(body: TokenRefrehIn, db: DB):
    try:
        payload = jwt.decode(body.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        data = TokenPayload(**payload)
        if data.type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        user_id = int(data.sub)
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    user = await db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found on database or inactive account")
    heimdall.info_log(F"Mercurius API Server :: HTTP POST::({user.email}) "
                      F"Refreshed Token")
    return create_token_pair(cast(int, cast(object, user.id)))

@mercurius.app_server.get("/users/me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_me(current_user: CurrentUser):
    heimdall.info_log(F"Mercurius API Server :: HTTP GET::({current_user.email}) "
                      F"Fetched Current User Profile: {current_user.email}")
    return current_user

@mercurius.app_server.get("/users", response_model=list[UserOut], status_code=status.HTTP_200_OK)
async def get_users(db: DB, current_user:  Annotated[User,
Depends(require_roles("admin", "root"))]):
    sql_statement = select(User).order_by(User.id.desc())
    result = await db.execute(sql_statement)
    heimdall.info_log(F"Mercurius API Server :: HTTP GET::({current_user.email}:{current_user.role}) "
                      F"Fetched All Users")
    return result.scalars().all()

## API CRUD Routes
@mercurius.app_server.post("/artifacts", response_model=ArtifactOut, status_code=status.HTTP_201_CREATED)
async def create_artifact(artifact_in: ArtifactCreate, db: DB, current_user: CurrentUser):
    artifact = Artifact(title=artifact_in.title, type=artifact_in.type, content=artifact_in.content,
                        owner_id=current_user.id)
    db.add(artifact)
    await db.commit()
    await db.refresh(artifact)
    heimdall.info_log(F"Mercurius API Server :: HTTP POST::({current_user.email}) "
                      F"Created New Artifact: {artifact.title} @ {artifact.created_at}")
    return artifact

@mercurius.app_server.get("/artifacts", response_model=list[ArtifactOut], status_code=status.HTTP_200_OK)
async def get_my_artifacts(db: DB, current_user: CurrentUser):
    sql_statement = (select(Artifact).options(joinedload(Artifact.owner)).where(Artifact.owner_id == current_user.id)
                     .order_by(Artifact.id.desc()))
    result = await db.execute(sql_statement)
    heimdall.info_log(F"Mercurius API Server :: HTTP GET::({current_user.email}) "
                      F"Fetched All User Artifacts")
    return result.scalars().all()

@mercurius.app_server.get("/artifacts-all", response_model=list[ArtifactOut], status_code=status.HTTP_200_OK)
async def get_all_artifacts(db: DB, current_user: Annotated[User,
Depends(require_roles("admin", "root"))]):
    sql_statement = select(Artifact).options(joinedload(Artifact.owner)).order_by(Artifact.id.desc())
    result = await db.execute(sql_statement)
    heimdall.info_log(F"Mercurius API Server :: HTTP GET::({current_user.email}:{current_user.role}) "
                      F"Fetched All Artifacts")
    return result.scalars().all()

@mercurius.app_server.get("/artifacts/{artifact_id}", response_model=ArtifactOut, status_code=status.HTTP_200_OK)
async def get_my_artifact(artifact_id: int, db: DB, current_user: CurrentUser):
    artifact = await db.get(Artifact, artifact_id)
    if not artifact or artifact.owner_id != current_user.id:
        heimdall.info_log(
            F"Mercurius API Server :: HTTP GET::({current_user.email}) "
            F"User Artifact By ID({artifact_id}) Not Found ")
        raise HTTPException(status_code=404, detail=F"Artifact not found for user ({artifact.owner})")
    await db.refresh(artifact, attribute_names=["owner"])
    heimdall.info_log(
        F"Mercurius API Server :: HTTP GET::({current_user.email}) Fetched User Artifact By ID ({artifact_id})")
    return artifact

@mercurius.app_server.get("/artifacts-any/{artifact_id}", response_model=ArtifactOut,
                          status_code=status.HTTP_200_OK)
async def get_any_artifact(artifact_id: int, db: DB, current_user: Annotated[User,
Depends(require_roles("admin", "root"))]):
    artifact = await db.get(Artifact, artifact_id)
    if not artifact:
        heimdall.info_log(
            F"Mercurius API Server :: HTTP GET::({current_user.email}) "
            F"* Artifact By ID({artifact_id}) Not Found ")
        raise HTTPException(status_code=404, detail=F"Artifact not found")
    await db.refresh(artifact, attribute_names=["owner"])
    heimdall.info_log(
        F"Mercurius API Server :: HTTP GET::({current_user.email}) Fetched * Artifact By ID ({artifact_id})")
    return artifact

@mercurius.app_server.delete("/artifacts/{artifact_id}", status_code=status.HTTP_200_OK)
async def delete_my_artifact(artifact_id: int, db: DB, current_user: CurrentUser):
    artifact = await db.get(Artifact, artifact_id)
    if not artifact or artifact.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail=F"Artifact not found")
    await db.delete(artifact)
    await db.commit()
    heimdall.info_log(F"Mercurius API Server :: HTTP DELETE::({current_user.email}) Deleted User Artifact By ID "
                      F"({artifact_id})")
    return artifact

@mercurius.app_server.delete("/artifacts-any/{artifact_id}", status_code=status.HTTP_200_OK)
async def delete_any_artifact(artifact_id: int, db: DB, current_user:  Annotated[User,
Depends(require_roles("admin", "root"))]):
    artifact = await db.get(Artifact, artifact_id)
    if not artifact:
        raise HTTPException(status_code=404, detail=F"Artifact not found")
    if current_user.role != "admin" or "root":
        raise HTTPException(status_code=401, detail="Access Unauthorized")
    await db.delete(artifact)
    await db.commit()
    heimdall.info_log(F"Mercurius API Server :: HTTP DELETE::({current_user.email}) Deleted Artifact By ID "
                      F"({artifact_id})")
    return artifact

@mercurius.app_server.delete("/artifacts", status_code=status.HTTP_200_OK)
async def delete_all_my_artifact(artifact_id: int, db: DB, current_user: CurrentUser):
    await db.execute(select(Artifact).where(Artifact.owner_id == current_user.id))
    await db.execute(Artifact.__table__.delete().where(Artifact.id == artifact_id))
    await db.commit()
    heimdall.info_log(F"Mercurius API Server :: HTTP DELETE::({current_user.email}) Deleted All User Artifacts")
    return {"action": "delete", "type": "owner", "user": current_user.email}

@mercurius.app_server.delete("/artifacts-any", status_code=status.HTTP_200_OK)
async def delete_all_any_artifact(db: DB, current_user: Annotated[User,
Depends(require_roles("admin", "root"))]):
    await db.execute(Artifact.__table__.delete())
    await db.commit()
    heimdall.info_log(F"Mercurius API Server :: HTTP DELETE::({current_user.email}) Deleted * Artifacts")
    return {"action": "delete", "type": "admin", "user": current_user.email}

@mercurius.app_server.get("/la-li-lu-le-lo")
async def get_la_li_lu_le_lo(current_user: CurrentUser):
    heimdall.info_log(F"Mercurius API Server :: HTTP GET::La Li Lu Le Lo ({current_user.email})")
    return {"mekagodzilla": "online", "user": current_user.email, "platform": Artisan.get_platform(),
            "platform_id": Artisan().userid}

@mercurius.app_server.get("/")
async def get_root_page():
    heimdall.info_log("Mercurius API Server :: HTTP GET::Root Page")
    return {"ok": True, "name": "MekaGodzilla RPA Server"}

## API Root Admin Routes

@mercurius.app_server.get("/admin/ping")
async def admin_ping(current_user: Annotated[User, Depends(require_roles("admin"))]):
    heimdall.info_log(F"Mercurius API Server :: HTTP GET::Admin Ping ({current_user.email})")
    return {"ok": True, "user": current_user.email, "role": current_user.role, "is_admin": True}

@mercurius.app_server.get("/root/ping")
async def admin_ping(current_user: Annotated[User, Depends(require_roles("root"))]):
    heimdall.info_log(F"Mercurius API Server :: HTTP GET::Root Ping ({current_user.email})")
    return {"ok": True, "user": current_user.email, "role": current_user.role, "is_root": True}

@mercurius.app_server.get("/administrator/root")
async def administrator_root(current_user: Annotated[User, Depends(require_roles("root"))]):
    heimdall.info_log(F"Mercurius API Server :: HTTP GET::Administrator Root ({current_user.email})")
    return {"mekagodzilla": "Root access granted", "user": current_user.email, "role": current_user.role}


""" FastAPI (async) + SQLite (aiosqlite) + JWT Authentication
Lightweight, single-file async FastAPI app with .env support. Includes: • User registration & login (bcrypt hashed passwords) • Access + refresh JWTs • Authenticated current user endpoint • Example Item CRUD (user-owned) • SQLite via SQLAlchemy 2.0 Async ORM • CORS + simple rate limiting
Run: python main.py
Install deps: pip install fastapi uvicorn[standard] sqlalchemy aiosqlite passlib[bcrypt] python-jose[cryptography] python-dotenv
Security notes:
Edit your .env file to set SECRET_KEY and other values.
Do NOT check .env into public repos. """