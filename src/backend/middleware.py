from typing import override

from flask import request
from backend.auth import get_jwt
from lib.front.middleware import IRequestMiddleware


def _append_path(required_path: str, *exclusions: str) -> set[str]:
    if required_path == "":
        return set(exclusions)
    return set(required_path + excl for excl in exclusions)


class AuthMiddleware(IRequestMiddleware):
    def __init__(self, *exclusions: str, required_path: str = "") -> None:
        self.__required_path: str = required_path
        self.__exclusions: set[str] = _append_path(self.__required_path, *exclusions)

    @override
    def process(self) -> bool:
        path: str = request.path

        if not path.startswith(self.__required_path):  # enforce only on required_path
            return True

        if path in self.__exclusions:  # ensures we should apply auth
            return True

        return get_jwt(disable_checks=False) is not None

    @override
    def abort_code(self) -> int:
        return 401
