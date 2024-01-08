import logging
import ssl
from typing import Annotated, List, Optional

import jwt
from config import get_settings
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OpenIdConnect,
)
from pydantic import BaseModel

ssl_ctx = ssl._create_unverified_context()

logger = logging.getLogger("uvicorn")
settings = get_settings()

openid = OpenIdConnect(openIdConnectUrl='https://auth.service.monema.dev/realms/upstash/.well-known/openid-configuration')

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)

class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication"
        )


class User(BaseModel):
    user_id: str
    username: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    scopes: List[str] = []
    roles: List[str] = []
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None

async def get_current_user(authHeader: Annotated[str, Depends(openid)]):
    if authHeader is None:
        raise UnauthenticatedException

    token = authHeader.split(' ')[1]

    if token is None:
        raise UnauthenticatedException
    domain = "auth.service.monema.dev"
    jwks_url = f'https://{domain}/realms/upstash/protocol/openid-connect/certs'
    jwks_client = jwt.PyJWKClient(jwks_url, ssl_context=ssl_ctx)
    # jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
    # jwks = json.loads(jsonurl.read())
        # This gets the 'kid' from the passed token
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(
            token
        ).key
    except jwt.exceptions.PyJWKClientError as error:
        raise UnauthorizedException(str(error))
    except jwt.exceptions.DecodeError as error:
        raise UnauthorizedException(str(error))

    try:
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=settings.auth_algorithms,
            audience=settings.auth_api_audience,
            issuer=settings.auth_issuer,
        )
        username: str = payload.get("preferred_username")
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        email_verified: str = payload.get("email_verified")
        # scope: str = payload.get("scope")
        scopes: List[str] = payload.get("scope").split(" ")
        name: str = payload.get("name")
        given_name: str = payload.get("given_name")
        family_name: str = payload.get("family_name")

        return User(
            user_id=user_id,
            username=username,
            email=email,
            scopes=scopes,
            roles=[],
            email_verified=email_verified,
            name=name,
            given_name=given_name,
            family_name=family_name,
        )
    except Exception as error:
        raise UnauthorizedException(str(error))


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user
