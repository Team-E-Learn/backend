from typing import override

from flask import request
from backend.auth import get_jwt
from lib.front.middleware import IRequestMiddleware
from lib.jwt.jwt import JwtValidator


class AuthMiddleware(IRequestMiddleware):

    def __init__(self, *exclusions: str) -> None:
        self.__exclusions: set[str] = set(exclusions)

    @override
    def process(self) -> bool:
        if request.path in self.__exclusions:  # ensures we should apply auth
            return True

        validator: JwtValidator | None = get_jwt()

        return validator is not None

    @override
    def abort_code(self) -> int:
        return 401
