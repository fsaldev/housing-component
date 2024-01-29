from datetime import datetime
from enum import Enum
import logging
from typing import Annotated
import requests
from fastapi import Depends, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from pydantic import BaseModel

from housing_component.core.errors import AuthErrors
from housing_component.settings import (
    ACCESS_TOKEN_ALGORITHM,
    ACCESS_TOKEN_AUDIENCE,
    ACCESS_TOKEN_ISSUER,
    ACCESS_TOKEN_LEEWAY,
    ACCESS_TOKEN_SECRET_KEY,
    SESSION_URL,
    KIWI_USERNAME,
    KIWI_PASSWORD,
)

log = logging.getLogger(__name__)


class AccessTokenContext(str, Enum):
    ORGANIZATION = "organization"
    SYSTEM = "system"


class AccessToken(BaseModel):
    user_id: int
    issued_at: datetime
    expiration_time: datetime
    context: AccessTokenContext
    organization_id: int | None


def require_access_token(
    auth: Annotated[
        HTTPAuthorizationCredentials,
        Depends(HTTPBearer(scheme_name="Access Token", auto_error=False)),
    ]
) -> AccessToken:
    if not auth:
        raise AuthErrors.UNAUTHORIZED

    try:
        payload = jwt.decode(
            auth.credentials,
            key=ACCESS_TOKEN_SECRET_KEY,
            algorithms=[ACCESS_TOKEN_ALGORITHM],
            issuer=ACCESS_TOKEN_ISSUER,
            audience=ACCESS_TOKEN_AUDIENCE,
            leeway=ACCESS_TOKEN_LEEWAY,
        )
    except jwt.InvalidTokenError:
        raise AuthErrors.ACCESS_TOKEN_INVALID

    try:
        return AccessToken(
            user_id=payload["sub"],
            issued_at=payload["iat"],
            expiration_time=payload["exp"],
            context=payload["ctx"],
            organization_id=payload.get("org"),
        )
    except (KeyError, ValueError):
        log.warn("Received access token with invalid payload", exc_info=True)
        raise AuthErrors.ACCESS_TOKEN_INVALID


def require_system_access_token(
    access_token: Annotated[AccessToken, Depends(require_access_token)]
) -> None:
    if access_token.context != AccessTokenContext.SYSTEM:
        raise AuthErrors.FORBIDDEN


def require_organization_access_token(
    organization_id: Annotated[int, Path()],
    access_token: Annotated[AccessToken, Depends(require_access_token)],
) -> None:
    if access_token.context == AccessTokenContext.SYSTEM:
        return

    if (
        access_token.context != AccessTokenContext.ORGANIZATION
        or organization_id != access_token.organization_id
    ):
        raise AuthErrors.FORBIDDEN_ORGANIZATION


def get_session_key() -> str | None:
    data = {"password": KIWI_USERNAME, "username": KIWI_PASSWORD}
    resp = requests.post(SESSION_URL, json=data)
    if resp.status_code != 200:
        return None
    resp_json = resp.json().get("result", {})
    return resp_json.get("session_key")
