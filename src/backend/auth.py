from flask import request

from lib.jwt.jwt import JwtValidator
from projenv import JWT_ACCESS_KEY


def get_jwt() -> JwtValidator | None:
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

    # Returns None if invalid token
    return JwtValidator.str_load(token, JWT_ACCESS_KEY)
