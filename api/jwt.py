from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import graphene
import jwt
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import get_user_model

USER = get_user_model()

JWT_ALGORITHM = "HS256"
JWT_AUTH_HEADER = "HTTP_AUTHORIZATION"
# JWT_CHAT_TOKEN = "HTTP_CHATTOKEN"
JWT_AUTH_HEADER_PREFIX = "BEARER"
JWT_ACCESS_TYPE = "access"
# JWT_REFRESH_TYPE = "refresh"
JWT_THIRDPARTY_ACCESS_TYPE = "thirdparty"
# JWT_REFRESH_TOKEN_COOKIE_NAME = "refreshToken"

PERMISSIONS_FIELD = "permissions"


def jwt_base_payload(exp_delta: timedelta) -> Dict[str, Any]:
    utc_now = datetime.utcnow()
    payload = {"iat": utc_now, "exp": utc_now + exp_delta}
    return payload


def jwt_user_payload(
        user: USER,
        token_type: str,
        exp_delta: timedelta,
        additional_payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload = jwt_base_payload(exp_delta)
    payload.update(
        {
            "token": user.jwt_token_key,
            "username": user.username,
            "type": token_type,
            "user_id": graphene.Node.to_global_id("User", user.id),
            "is_staff": user.is_staff,
        }
    )
    if additional_payload:
        payload.update(additional_payload)
    return payload


def jwt_encode(payload: Dict[str, Any]) -> str:
    return jwt.encode(
        payload,
        settings.SECRET_KEY,  # type: ignore
        JWT_ALGORITHM,
    )


def jwt_decode(token: str) -> Dict[str, Any]:
    return jwt.decode(
        token,
        settings.SECRET_KEY,  # type: ignore
        algorithms=[JWT_ALGORITHM],
        verify_expiration=settings.JWT_EXPIRE,
    )


def create_token(payload: Dict[str, Any], exp_delta: timedelta) -> str:
    payload.update(jwt_base_payload(exp_delta))
    return jwt_encode(payload)


def create_access_token(
        user: USER, additional_payload: Optional[Dict[str, Any]] = None
) -> str:
    payload = jwt_user_payload(
        user, JWT_ACCESS_TYPE, settings.JWT_TTL_ACCESS, additional_payload
    )
    return jwt_encode(payload)


# def create_refresh_token(
#         user: USER, additional_payload: Optional[Dict[str, Any]] = None
# ) -> str:
#     payload = jwt_user_payload(
#         user,
#         JWT_REFRESH_TYPE,
#         settings.JWT_TTL_REFRESH,
#         additional_payload,
#     )
#
#     return jwt_encode(payload)


def get_token_from_request(request: WSGIRequest) -> Optional[str]:
    auth = request.META.get(JWT_AUTH_HEADER, "").split(maxsplit=1)
    prefix = JWT_AUTH_HEADER_PREFIX

    if len(auth) != 2 or auth[0].upper() != prefix:
        return None
    return auth[1]

#
# def get_chat_token_from_request(request: WSGIRequest) -> Optional[str]:
#     chat_token_auth = request.META.get(JWT_CHAT_TOKEN)
#     return chat_token_auth


def get_user_from_payload(payload: Dict[str, Any]) -> Optional[USER]:
    user_qs = USER.objects.filter(username=payload["username"])
    user_obj = user_qs.first()
    user_jwt_token = payload.get("token")
    if user_obj is not None:
        if user_obj.is_blocked:
            raise ValidationError("Your account has been inactivated, kindly contact your administrator.")
    user = user_qs.filter(is_active=True).first()
    if not user_jwt_token or not user:
        raise jwt.InvalidTokenError(
            "Invalid token. Create new one by using tokenCreate mutation."
        )
    return user


def get_user_from_access_token(token: str) -> Optional[USER]:
    payload = jwt_decode(token)
    jwt_type = payload.get("type")
    if jwt_type not in [JWT_ACCESS_TYPE, JWT_THIRDPARTY_ACCESS_TYPE]:
        raise jwt.InvalidTokenError(
            "Invalid token. Create new one by using tokenCreate mutation."
        )
    user = get_user_from_payload(payload)
    return user


def jwt_card_payload(
        card_details,
        exp_delta: timedelta,
        additional_payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload = jwt_base_payload(exp_delta)
    payload.update(
        {
            "card": card_details.number,
            "exp_month": card_details.exp_month,
            "exp_year": card_details.exp_year,
            "cvv": card_details.cvv
        }
    )
    if additional_payload:
        payload.update(additional_payload)
    return payload
