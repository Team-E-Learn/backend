from time import time
from flask import request

from lib.jwt.jwt import ALLOWED_CLAIM_DATA, JwtValidator
from projenv import JWT_ACCESS_KEY


def get_jwt_sub(validator: JwtValidator | None = None) -> int | None:
    if (jwt := validator or get_jwt()) is None:
        return None

    try:
        return int(jwt.get_payload()["sub"])
    except KeyError | ValueError | TypeError:
        return None


def get_jwt_exp(validator: JwtValidator | None = None) -> int | None:
    if (jwt := validator or get_jwt()) is None:
        return None

    try:
        return int(jwt.get_payload()["exp"])
    except KeyError | ValueError | TypeError:
        return None


def valid_jwt_sub(found_id: int) -> bool:
    if sub_id := get_jwt_sub() is None:
        return False
    return sub_id == found_id


def get_jwt(
    disable_checks: bool = True, required_aud: str = "elearn-full"
) -> JwtValidator | None:
    # get the header for Authorization
    auth_header: str | None = request.headers.get("Authorization")

    if auth_header is None:  # header not found- invalid
        return None

    # format should be "Bearer <token here>"
    split: list[str] = auth_header.split(" ", maxsplit=1)

    if len(split) != 2:
        return None

    bearer, token = split

    if bearer != "Bearer":
        return None

    validator: JwtValidator | None = JwtValidator.str_load(token, JWT_ACCESS_KEY)

    if validator is None:
        return None

    payload: dict[str, ALLOWED_CLAIM_DATA] = validator.get_payload()

    # The backend requires both sub and exp to exist
    if disable_checks:
        return validator

    try:
        iss: str = str(payload["iss"])
        aud: str = str(payload["aud"])
        _ = int(payload["sub"])
        exp: int = int(payload["exp"])
    except KeyError | ValueError:
        return None

    if iss != "elearn-backend":
        return None

    if aud != required_aud:
        return None

    if int(time()) > exp:  # check if the token has expired
        return None

    return validator
