# FastAPI (Concurrent) API Server
from __future__ import annotations
import asyncio
import multiprocessing
import time
from typing import cast, Set, Optional
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from artificer.artificer import ASCI_BLUE, ASCI_ARROW, ASCI_RESET, ASCI_TEAL, ASCI_MERCURY, ASCI_GREEN, ASCI_POWER
import os
from typing import Annotated, AsyncGenerator
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, joinedload

from artisan.hermes import Hermes
from mercurius.db_models import User
from mercurius.db_models import Artifact
from mercurius.http_models import Token, TokenPayload, TokenRefreshIn, UserCreate, UserOut, ArtifactCreate, ArtifactOut
from mercurius.http_models_rpa import RPAResponseOut, TACOSCreateAccountDemoRPARequest, \
    GlobalGatewayGetAccountRPARequest, GlobalGatewayCreateTestEntityRPARequest
from mercurius.rate_limiter_middleware import RateLimiterMiddleware
from mercurius.tools import verify_password, get_password_hash, create_token_pair
from artisan.artisan import Artisan
from heimdall.heimdall import Heimdall
from prometheus.prometheus_fire import PrometheusFire
from trulioome.trulioome import TruliooME

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
VERSION = os.getenv("VERSION", "MekaGodzilla")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

chrome_options = ChromeOptions()
firefox_options = FirefoxOptions()
if os.getenv("PROMETHEUS_HEADLESS_MODE") == "True":
    chrome_options.add_argument("--headless=new")
    firefox_options.add_argument("--headless")
artisan = Artisan()

class Mercurius:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(Mercurius, cls).__new__(cls)
        return cls._instance  # Always return the existing instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.app_server = FastAPI(title="Mercurius", description="MekaGodzilla RPA Server API")
            self.version = VERSION
            self.environment = ENVIRONMENT
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

    @staticmethod
    def get_webdriver() -> WebDriver:
        prometheus_driver = None
        match os.getenv("PROMETHEUS_DEFAULT_DRIVER").lower():
            case "chrome":
                prometheus_driver = webdriver.Chrome(options=chrome_options)
                print("Value is chrome.")
            case "firefox":
                prometheus_driver = webdriver.Firefox(options=firefox_options)
                print("Value is firefox.")
            case "edge":
                prometheus_driver = webdriver.Edge(options=chrome_options)
            case _:  # Default case, similar to 'else'
                prometheus_driver = webdriver.Chrome(options=chrome_options)
                print("Value does not match any specific browser.")
        return prometheus_driver


heimdall = Heimdall()
mercurius = Mercurius()


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


mercurius.app_server.add_middleware(RateLimiterMiddleware, limit_per_min=RATE_LIMIT_PER_MIN)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
DB = Annotated[AsyncSession, Depends(get_db)]

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
async def refresh_tokens(body: TokenRefreshIn, db: DB):
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
        raise HTTPException(status_code=404, detail=F"Artifact not found for user ({current_user.email})")
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
    await db.delete(artifact)
    await db.commit()
    heimdall.info_log(F"Mercurius API Server :: HTTP DELETE::({current_user.email}) Deleted Artifact By ID "
                      F"({artifact_id})")
    return artifact

@mercurius.app_server.delete("/artifacts", status_code=status.HTTP_200_OK)
async def delete_all_my_artifact(db: DB, current_user: CurrentUser):
    await db.execute(select(Artifact).where(Artifact.owner_id == current_user.id))
    await db.execute(Artifact.__table__.delete().where(Artifact.owner_id == current_user.id))
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

@mercurius.app_server.get("/", response_model=RPAResponseOut,  status_code=status.HTTP_201_CREATED)
async def get_create_tacos_account_demo(global_gateway_create_account_user:
Optional[TACOSCreateAccountDemoRPARequest] = None):
    heimdall.info_log("Mercurius API Server :: HTTP GET::Create Tacos Account Demo")
    start_time = artisan.get_current_timestamp()
    rpa_webdriver = await PrometheusFire(heimdall=heimdall, fullscreen=True, headless=False).get_prometheus_webdriver()
    rpa_webdriver.fullscreen_window()
    rpa_username = os.getenv("GG_ADMIN_USERNAME")
    rpa_password = os.getenv("GG_ADMIN_PASSWORD")
    account_name = "MekaGodzilla Test" or "MekaTron Test"
    if global_gateway_create_account_user:
        if global_gateway_create_account_user.username:
            rpa_username = global_gateway_create_account_user.username
        if global_gateway_create_account_user.password:
            rpa_password = global_gateway_create_account_user.password
        if global_gateway_create_account_user.account_name:
            account_name = global_gateway_create_account_user.account_name
    create_account_demo = await TruliooME(heimdall=heimdall,
                                    web_driver=rpa_webdriver).tacos_create_account_demo(
        username=rpa_username,
        password=rpa_password,
        account_name=account_name,
        auth_mode=1)
    rpa_webdriver = create_account_demo[0]
    is_complete = create_account_demo[1]
    time.sleep(13)
    rpa_webdriver.quit()
    return {
            "action": F"Create Account Demo ({account_name})",
            "globalgateway_username": F"{rpa_username}",
            "is_complete": is_complete, "started_at": start_time,
            "completed_at": F"{artisan.get_current_timestamp()}",
            "execution_time": F"{artisan.get_time_delta(start_time=start_time, 
                    end_time=artisan.get_current_timestamp()).total_seconds()} seconds"}

@mercurius.app_server.get("/client-portal")
async def get_client_portal():
    heimdall.info_log("Mercurius API Server :: HTTP GET::LogIn Client Portal Page")
    rpa_web_driver = await PrometheusFire(fullscreen=True).client_portal_login(username=os.getenv("PORTAL_USERNAME"),
                                                                         password=os.getenv("PORTAL_PASSWORD"))

@mercurius.app_server.get("/global-gateway-account", response_model=RPAResponseOut, status_code=status.HTTP_200_OK)
async def get_global_gateway_admin_account(global_gateway_admin_account: GlobalGatewayGetAccountRPARequest):
    heimdall.info_log("Mercurius API Server :: HTTP GET::LogIn Client Portal Page")
    start_time = artisan.get_current_timestamp()
    rpa_web_driver = await PrometheusFire(fullscreen=True).get_prometheus_webdriver()
    rpa_web_driver.fullscreen_window()
    rpa_username = os.getenv("GG_ADMIN_USERNAME")
    rpa_password = os.getenv("GG_ADMIN_PASSWORD")
    account_name = global_gateway_admin_account.account_name
    if global_gateway_admin_account:
        if global_gateway_admin_account.username:
            rpa_username = global_gateway_admin_account.username
        if global_gateway_admin_account.password:
            rpa_password = global_gateway_admin_account.password
    global_gateway_legacy = await TruliooME(
        heimdall=heimdall,
        web_driver=rpa_web_driver).global_gateway_legacy_login(
        username=rpa_username,
        password=rpa_password,
        auth_mode=1)
    rpa_web_driver = global_gateway_legacy[0]
    is_complete = global_gateway_legacy[1]
    if is_complete:
        go_to_account_request = await TruliooME(
            heimdall=heimdall,
            web_driver=rpa_web_driver).go_to_legacy_account_by_name_or_identifier(
            account_name=account_name)
        is_complete = go_to_account_request[1]
    return {"action": F"Go to Global Gateway Admin Account ({account_name})",
            "globalgateway_username": F"{rpa_username}",
            "is_complete": is_complete,
            "started_at": start_time,
            "completed_at": F"{artisan.get_current_timestamp()}",
            "execution_time": F"{artisan.get_time_delta(
                start_time=start_time, end_time=artisan.get_current_timestamp()).total_seconds()} seconds"}

@mercurius.app_server.get("/gg-account-testentity", response_model=RPAResponseOut,
                          status_code=status.HTTP_201_CREATED)
async def create_gg_account_test_entity(global_gateway_account_testentity: GlobalGatewayCreateTestEntityRPARequest):
    account_name = ""
    is_complete = False
    start_time = artisan.get_current_timestamp()
    rpa_web_driver = await PrometheusFire(fullscreen=True).get_prometheus_webdriver()
    rpa_web_driver.fullscreen_window()
    rpa_username = os.getenv("GG_ADMIN_USERNAME")
    rpa_password = os.getenv("GG_ADMIN_PASSWORD")
    entity_type = global_gateway_account_testentity.entity_type
    account_name = global_gateway_account_testentity.account_name
    if global_gateway_account_testentity:
        if global_gateway_account_testentity.username:
            rpa_username = global_gateway_account_testentity.username
        if global_gateway_account_testentity.password:
            rpa_password = global_gateway_account_testentity.password
        if global_gateway_account_testentity.entity_type not in ["KYC", "KYB"]:
            entity_type = "KYC"
    global_gateway_legacy = await TruliooME(
        heimdall=heimdall,
        web_driver=rpa_web_driver).global_gateway_legacy_login(
        username=rpa_username,
        password=rpa_password,
        auth_mode=1)
    rpa_web_driver = global_gateway_legacy[0]
    is_logged_in = global_gateway_legacy[1]
    if is_logged_in:
        go_to_account_request = await TruliooME(
            heimdall=heimdall,
            web_driver=rpa_web_driver).go_to_legacy_account_by_name_or_identifier(
            account_name=account_name)
        is_target_account = go_to_account_request[1]
        if is_target_account:
            create_account_test_entity = await TruliooME(
                heimdall=heimdall,
                web_driver=rpa_web_driver).create_global_gateway_account_test_entity(
                entity_type=entity_type,
                country=global_gateway_account_testentity.country,
                entity_name=global_gateway_account_testentity.entity_name)
            is_complete = create_account_test_entity[1]

    return {"action": F"Create {Hermes.get_country_code(global_gateway_account_testentity.country)} "
                      F"{entity_type} "
                      F"Account ({account_name}) Test Entity ({global_gateway_account_testentity.entity_name})",
            "globalgateway_username": F"{rpa_username}",
            "is_complete": is_complete,
            "started_at": start_time,
            "completed_at": F"{artisan.get_current_timestamp()}",
            "execution_time": F"{artisan.get_time_delta(
                start_time=start_time, end_time=artisan.get_current_timestamp()).total_seconds()} seconds"}
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