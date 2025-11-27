# Trulioo API Interface Interactions
from __future__ import annotations

import json
from typing import Optional

from artificer.artificer import ASCI_BLUE, ASCI_RESET, ASCI_ARROW
from artisan.artisan import Artisan
from soteria.api_client_key import ApiClientKeyAuth
from soteria.api_client_oauth2 import ApiClientOAuth2
import os
from dotenv import load_dotenv

from soteria.api_client_token import ApiClientTokenAuth
from soteria.api_error import ApiError

load_dotenv(verbose=True)

class Soteria:
    _instance = None
    """
    Asynchronous Soteria API Client
    - Injectable AuthStrategy
    - Strategies: ApiKey, Bearer Token, OAuth2ClientCredentials, HMAC Authentication
    - Retries w/ exponential backoff
    - Optional QPS functionality (client-wide rate limiting)
    """

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(Soteria, cls).__new__(cls)
        return cls._instance  # Always return the existing instance

    def __init__(self, heimdall):
        if not hasattr(self, '_initialized'):
            self.artisan = Artisan()
            self.heimdall = heimdall
            self.auth_token = None
            self.token_api_client =  ApiClientTokenAuth(base_url=os.getenv('SOTERIA_BASE_URL'))
            self.oauth2_api_client = ApiClientOAuth2(base_url=os.getenv('SOTERIA_BASE_URL'),
                                                token_url=os.getenv('SOTERIA_AUTH_URL'),
                                                client_id=os.getenv('SOTERIA_CLIENT_ID'),
                                                client_secret=os.getenv('SOTERIA_CLIENT_SECRET'),)
            self.webhook_client = ApiClientKeyAuth(base_url=os.getenv('WEBHOOKS_SERVICE_BASEURL'),
                                                   api_key=os.getenv('WEBHOOKS_API_KEY'),
                                                   header_name="API-Key")
            self.webhook_ids = []
            self._initialized = True
            self.heimdall.info_log(F"Initialized Soteria T-NAPI Interface::{self.artisan.userid}@trulioo.com")
            print(F"{ASCI_BLUE}{ASCI_ARROW} Soteria Initialized{ASCI_RESET}")

    # Trulioo Platform API
    async def authenticate(self):
        try:
            self.auth_token = await self.oauth2_api_client.authenticate()
            await self.token_api_client.authenticate_form(auth_path=os.getenv('SOTERIA_AUTH_URL'),
                                                          login_body={"client_id": os.getenv('SOTERIA_CLIENT_ID'),
                                                                      "client_secret":
                                                                          os.getenv('SOTERIA_CLIENT_SECRET'),
                                                                      "grant_type": "client_credentials"})
            return self.auth_token
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Authentication Error :: {e.status_code}:{e.body}")
            print(F"Soteria Authentication Error :: {e.status_code}:{e.body}")
        finally:
            if self.auth_token:
                self.heimdall.info_log(F"Trulioo API Authentication Token :: {self.auth_token}")
            else:
                self.heimdall.error_log(F"Trulioo API Authentication Token Not Found")
            return self.auth_token

    async def initialize_workflow(self, flow_id):
        response = None
        try:
            response = await self.oauth2_api_client.http_get(path=F"/wfs/interpreter-v2/flow/{flow_id}")
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Initialize Workflow ({flow_id}) Error :: {e.status_code}:{e.body}")
            print(F"Soteria Initialize Workflow Error ({flow_id}) :: {e.status_code}:{e.body}")
        finally:
            if response:
                self.heimdall.info_log(F"Trulioo API Initialize Workflow ({flow_id}) :: Response :{response.json()}")
            else:
                self.heimdall.error_log(F"Trulioo API Initialize Workflow ({flow_id}) Response Not Found")


    async def submit_initialized_workflow_data(self, flow_id, flow_json_data):
        response = None
        try:
            response = await self.oauth2_api_client.http_post(path=F"/wfs/interpreter-v2/submit/{flow_id}",
                                                   body=json.dumps(flow_json_data))
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Submit Initialized Workflow ({flow_id}) Error :: "
                                    F"{e.status_code}:{e.body}")
            print(F"Soteria Submit Initialized Workflow ({flow_id}) Error :: {e.status_code}:{e.body}")
        finally:
            if response:
                self.heimdall.info_log(F"Trulioo API Submit Initialized Workflow ({flow_id}) Data "
                                       F"({json.dumps(flow_json_data)}) :: Response :{response.json()}")
            else:
                self.heimdall.error_log(F"Trulioo API Submit Initialized Workflow ({flow_id}) Data Response Not Found")

    async def get_initialized_workflow_step(self, flow_id, x_hf_session, x_hf_language="en-US"):
        response = None
        try:
            response = await self.oauth2_api_client.http_get(path=F"/wfs/interpreter-v2/flow/{flow_id}",
                                            headers={"x_hf_session": x_hf_session,
                                                     "x_hf_language": x_hf_language})
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Get Initialized Workflow Step ({flow_id}) Error :: "
                                    F"{e.status_code}:{e.body}")
            print(F"Soteria Get Initialized Workflow Step ({flow_id}) Error :: "
                  F"{e.status_code}:{e.body}")
        finally:
            if response:
                self.heimdall.info_log(F"Trulioo API Get Initialized Workflow Step ({flow_id})<{x_hf_session}>  "
                                       F":: Response :{response.json()}")
            else:
                self.heimdall.error_log("Trulioo API Get Initialized Workflow Step Response Not Found")

    async def get_workflows_by_wfs_client_id(self, x_hf_session):
        response = None
        try:
            response = await self.oauth2_api_client.http_get(path=F"/wfs/export/v2/query/client/{x_hf_session}",)
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Get Workflows by WFS Client ID ({x_hf_session}) Error :: "
                                    F"{e.status_code}:{e.body}")
            print(F"Soteria Get Workflows by WFS Client ID ({x_hf_session}) Error :: "
                                    F"{e.status_code}:{e.body}")
        finally:
            if response:
                self.heimdall.info_log(F"Trulioo API Get Workflows by WFS Client ID Response ({x_hf_session}) "
                                       F":: Response: {response.json()}")
            else:
                self.heimdall.error_log("Trulioo API Get Workflows Response Not Found")

    async def generate_signed_url_for_wf_session(self, flow_id, x_hf_session):
        response = None
        try:
            response = await self.oauth2_api_client.http_get(
                path=F"/wfs/interpreter-v2/signed-url/{flow_id}?endClientId={x_hf_session}",)
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Generate Workflow ({flow_id}) Signed URL for WF Session ({x_hf_session}) "
                                    F"Error :: {e.status_code}:{e.body}")
            print(F"Soteria Generate WF Signed URL ({flow_id}) Error :: {e.status_code}:{e.body}")
        finally:
            if response:
                self.heimdall.info_log(F"Trulioo API Generated Workflow ({flow_id}) Signed URL for WF Session "
                                       F"{x_hf_session} :: Response :{response.json()}")
            else:
                self.heimdall.error_log(F"Trulioo API Generate Workflow ({flow_id}) Session ({x_hf_session}) "
                                        F"Signed URL Response Not Found")

    # Normalized API (NAPI)

    async def get_workflow_test(self, flow_id):
        response = None
        try:
            response = await self.oauth2_api_client.http_get(path=F"/wfs/interpreter-v2/test/flow/{flow_id}",)
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Get Workflow Test ({flow_id}) Error :: {e.status_code}:{e.body}")
            print(F"Soteria Get Workflow Test ({flow_id}) Error :: {e.status_code}:{e.body}")
        finally:
            if response:
                self.heimdall.info_log(F"Trulioo API Get Workflow ({flow_id}) Test"
                                       F" :: Response :{response.json()}")
            else:
                self.heimdall.error_log(F"Trulioo API Get Workflow ({flow_id}) Test "
                                        F"Response Not Found")


    async def get_initialized_prefill_workflow_step(self, flow_id):
        response = None
        try:
            response = await self.oauth2_api_client.http_get(path=F"/interpreter-v2/init/{flow_id}",)
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Get Initialized Prefill Workflow ({flow_id}) Error :: "
                                    F"{e.status_code}:{e.body}")
            print(F"Soteria Get Initialized Prefill Workflow ({flow_id}) Error :: {e.status_code}:{e.body}")
        finally:
            if response:
                self.heimdall.info_log(F"Trulioo API Get Initialized Prefill Workflow ({flow_id}) :: "
                                       F"Response :{response.json()}")
            else:
                self.heimdall.error_log(F"Trulioo API Get Initialized Prefill Workflow ({flow_id}) Response Not Found")

    async def submit_initialized_prefill_workflow_data(self, flow_id, flow_json_data, x_hf_session):
        response = None
        try:
            response = await self.oauth2_api_client.http_post(path=F"/interpreter-v2/submit/{flow_id}",
                                             body=json.dumps(flow_json_data),
                                             headers={"x_hf_session": x_hf_session})
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Submit Initialized Prefill Workflow ({flow_id}) Error :: "
                                    F"{e.status_code}:{e.body}")
            print(F"Soteria Submit Initialized Prefill Workflow ({flow_id}) Error :: {e.status_code}:{e.body}")
        finally:
            if response:
                self.heimdall.info_log(F"Trulioo API Submitted Initialized Prefill Workflow "
                                       F"({flow_id})<{x_hf_session} > "
                                       F"Data ({json.dumps(flow_json_data)}) :: "
                                       F"Response :{response.json()}")
            else:
                self.heimdall.error_log(F"Trulioo API Submitted Initialized Prefill Workflow "
                                        F"({flow_id}) Response Not Found")

    async def get_packages_list(self):
        response = None
        try:
            response = await self.oauth2_api_client.http_get(path=F"/v3/account/packages")
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Get Packages List Error :: {e.status_code}:{e.body}")
            print(F"Soteria Get Packages List Error :: {e.status_code}:{e.body}")
        finally:
            if response:
                self.heimdall.info_log(F"Trulioo API Get Packages List Response :: Response :{response.json()}")
            else:
                self.heimdall.error_log(F"Trulioo API Get Packages List Response Not Found")

    async def get_package_fields(self, package_id, country_code):
        response = None
        try:
            response = await self.oauth2_api_client.http_get(path=F"/v3/configuration/fields/{package_id}/"
                                                                  F"{country_code}")
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Get Package Fields ({package_id}:{country_code}) Error :: "
                                    F"{e.status_code}:{e.body}")
            print(F"Soteria Get Package Fields ({package_id}:{country_code}) Error :: {e.status_code}:{e.body}")
        finally:
            if response:
                self.heimdall.info_log(F"Trulioo API Get Package Fields Response :: Response :{response.json()}")
            else:
                self.heimdall.error_log(F"Trulioo API Get Package Fields Response Not Found")

    async def get_package_test_entities(self, package_id, country_code):
        response = None
        try:
            response = await self.oauth2_api_client.http_get(path=F"/v3/configuration/testentities/{package_id}/"
                                                                  F"{country_code}")
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Get Package ({package_id}) Test Entities ({country_code}) Error :: "
                                    F"{e.status_code}:{e.body}")
            print(F"Soteria Get Package ({package_id}) Test Entities ({country_code}) Error :: "
                  F"{e.status_code}:{e.body}")
        finally:
            if response:
                self.heimdall.info_log(F"Trulioo API Get Package ({package_id}:{country_code}) Test Entities Response "
                                       F":: Response :{response.json()}")
            else:
                self.heimdall.error_log(F"Trulioo API Get Package ({package_id}:{country_code}) Test Entities Response "
                                        F"Not Found")

    # Webhooks
    async def create_new_webhook(self):
        response = None
        try:
            response = await self.webhook_client.http_post(path=F"/", body=None)
            webhook_id = response.json().get('uuid')
            self.webhook_ids.append(webhook_id)
            return self.webhook_ids[-1]
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Create New Webhook Error :: {e.status_code}:{e.body}")
            print(F"Soteria Create New Webhook Error :: {e.status_code}:{e.body}")
        finally:
            if response and response.status_code == 201:
                self.heimdall.info(f"Soteria Create New Webhook :: Response : {response.json().get('uuid')}) ")
            else:
                self.heimdall.error_log(F"Soteria Create New Webhook Response Not Found")


    async def set_wfs_challenge_response(self, webhook_id: Optional[str] = None):
        response = None
        if not webhook_id and len(self.webhook_ids) > 0:
            webhook_id = self.webhook_ids[-1]
        challenge_body = {
            "type": "modify_response",
            "condition": "null",
            "parameters": {
                "content": "$request.content$",
                "headers": "content-type: application/json"
            },
            "order": 1
        }
        try:
            response = await self.webhook_client.http_post(path=F"/{webhook_id}/actions",
                                                body=json.dumps(challenge_body))
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Set WFS Challenge Response Error ({webhook_id}) :: "
                                    F"{e.status_code}:{e.body}")
            print(F"Soteria Set WFS Challenge Response Error ({webhook_id}) :: "
                                    F"{e.status_code}:{e.body}")
        finally:
            if response and response.status_code == 201:
                self.heimdall.info_log(F"Soteria Set WFS Challenge Response :: Response: {response.json()})")
            else:
                self.heimdall.error_log("Soteria Set WFS Challenge Response Not Found")

    async def get_all_requests(self, webhook_id):
        response = None
        try:
            response = await self.webhook_client.http_get(path=F"/{webhook_id}/requests")
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Get All Requests ({webhook_id}) Error :: {e.status_code}:{e.body}")
            print(F"Soteria Get All Requests ({webhook_id}) Error :: {e.status_code}:{e.body}")
        finally:
            if response and response.status_code == 200:
                self.heimdall.info_log(F"Soteria Get All WebHook ID Requests ({webhook_id}) :: "
                                       F"Response: {response.json()})")
            else:
                self.heimdall.error_log(F"Soteria Get All WebHook ID Requests Response Not Found")

    async def get_request_by_id(self, webhook_id, request_id):
        response = None
        try:
            response = await self.webhook_client.http_get(path=F"/{webhook_id}/request/{request_id}")
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Get Request By Request ID ({request_id}) Error :: "
                                    F"{e.status_code}:{e.body}")
            print(F"Soteria Get Request By Request ID ({request_id}) Error :: {e.status_code}:{e.body}")
        finally:
            if response:
                self.heimdall.info_log(F"Soteria Get Webhook ({webhook_id}) Request By Request ID ({request_id}) :: "
                                       F"Response: {response.json()})")
            else:
                self.heimdall.error_log(F"Soteria Get Request By Request ID ({request_id}) Response Not Found")

    async def clear_all_requests(self, webhook_id):
        response = None
        try:
            response = await self.webhook_client.http_delete(path=F"/{webhook_id}/requests")
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Clear All Requests ({webhook_id}) Error :: {e.status_code}:{e.body}")
            print(F"Soteria Clear All Requests ({webhook_id}) Error :: {e.status_code}:{e.body}")
        finally:
            if response:
                self.heimdall.info_log(F"Soteria Clear All Webhook ({webhook_id}) Requests :: "
                                       F"Response : {response.json()})")
            else:
                self.heimdall.error_log(F"Soteria Clear All Webhook ({webhook_id}) Requests Response Not Found")

    async def delete_webhook(self, webhook_id):
        response = None
        try:
            response = await self.webhook_client.http_delete(path=F"/{webhook_id}")
            return response.json()
        except ApiError as e:
            self.heimdall.error_log(F"Soteria Delete Webhook ({webhook_id}) Error :: {e.status_code}:{e.body}")
            print(F"Soteria Delete Webhook ({webhook_id}) Error :: {e.status_code}:{e.body}")
        finally:
            if response:
                self.heimdall.info_log(F"Soteria Delete Webhook ({webhook_id}) :: Response : {response.json()})")
            else:
                self.heimdall.error_log(F"Soteria Delete Webhook ({webhook_id}) Response Not Found")













