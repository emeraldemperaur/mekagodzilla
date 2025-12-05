# HTTP RPA Request Schemas
from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional, Literal
import datetime as dt
from artisan.artisan import Artisan
from artisan.hermes import Hermes


class GlobalGatewayLoginRPARequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class GlobalGatewayGetAccountRPARequest(BaseModel):
    username: Optional[str] = None
    password: Optional[SecretStr] = None
    account_name: str
    account_identifier: Optional[str] = None
    email_address: Optional[str] = None
    sub_account_name: Optional[str] = None

class GlobalGatewayCreateTestEntityRPARequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    account_name: str
    country: str
    entity_name: str
    entity_type: Optional[Literal['KYC', 'KYB', 'None']] = None
    account_identifier: Optional[str] = None
    email_address: Optional[str] = None
    sub_account_name: Optional[str] = None

class TACOSCreateAccountDemoRPARequest(BaseModel):
    username: Optional[str] = None
    password: Optional[SecretStr] = None
    account_name: Optional[str] = None
    account_identifier: Optional[str] = None
    is_mfa: Optional[bool] = None
    is_internal: Optional[bool] = True
    is_sandbox: Optional[bool] = True
    allow_download: Optional[bool] = None
    reset_period: Optional[str | int] = None
    retention_period: Optional[str | int] = None

class TACOSCreatePackageRPARequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    account_name: str
    account_identifier: Optional[str] = None
    sf_account_id: Optional[str] = None
    description: Optional[str] = None
    service_name: str
    address_format: Optional[str] = None
    schedule_template: Optional[str] = None
    retention_period: Optional[str | int] = None
    countries: Optional[list] = None
    rules: Optional[list[dict]] = None

class TACOSCloneExtantPackageRPARequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    account_name: str
    account_identifier: Optional[str] = None
    sf_account_id: Optional[str] = None
    origin_account_name: str
    package_name: str
    clone_name: str
    enable: Optional[bool] = True

class TACOSCreateUserRPARequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    account_name: str
    account_identifier: Optional[str] = None
    user_email: EmailStr
    user_name: str
    first_name: str
    last_name: str
    status: bool
    roles: Optional[bool | list[dict]] = None

class TACOSCreateAPICredentialRPARequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    account_name: str
    account_identifier: Optional[str] = None
    credential_name: str
    status: Optional[bool | None] = None
    token_duration: int
    expiration_date: str
    is_internal: bool
    roles: Optional[bool | list[dict]] = None
    api_services: Optional[bool | list[dict]] = None
    access_all_packages: Optional[bool] = True
    transaction_type: Optional[str | int] = None

class TACOSCloneWorkflowRPARequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    origin_account_name: str
    workflow_name: str
    target_account_name: str

class ClientAdminUser(BaseModel):
    username: str
    password: str

class RPAResponseOut(BaseModel):
    rpa_server: Optional[str] = F"{Artisan.get_rpa_server_version()}"
    os_platform: Optional[str] = F"{Artisan.get_platform()}"
    action: str
    parameters: Optional[dict] = None
    globalgateway_username: Optional[str] = None
    clientadmin_username: Optional[str] = None
    is_complete: bool
    error_encountered: Optional[bool] = False
    started_at: str
    completed_at: Optional[str | None] = None
    execution_time: Optional[dt.timedelta | str | int | float | None] = None