from base64 import urlsafe_b64encode
from hashlib import sha256
import hmac
from json import dumps
from typing import override


def _hash_msg(msg: bytes, key: bytes) -> str:
    hash_: bytes = hmac.new(key=key, msg=msg, digestmod=sha256).digest()
    return urlsafe_b64encode(hash_).decode().strip("=")


def _encode(string: str) -> str:
    return urlsafe_b64encode(bytes(string, "latin-1")).decode().strip("=")


class Jwt:

    def __init__(self, key: bytes) -> None:
        self.__key: bytes = key
        self.__claims: dict[str, str] = {}

    def add_claim(self, name: str, value: str) -> "Jwt":
        self.__claims[name] = value
        return self

    def sign(self) -> str:
        return f"{self.__head()}.{self.__payload()}.{self.__signature()}"

    def __head(self) -> str:
        data: str = dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":"))
        return _encode(data)

    def __payload(self) -> str:
        data: str = dumps(self.__claims, separators=(",", ":"))
        return _encode(data)

    def __signature(self) -> str:
        return _hash_msg(
            bytes(self.__head() + "." + self.__payload(), "latin-1"), self.__key
        )

    @staticmethod
    def validate(head: str, payload: str, sig: str, key: bytes) -> bool:
        msg: bytes = bytes(f"{head}.{payload}", "latin-1")
        return _hash_msg(msg, key) == sig

    @staticmethod
    def validate_token(token: str, key: bytes) -> bool:
        if token.count(".") != 2:
            return False

        header, payload, signature = token.split(".")
        return Jwt.validate(header, payload, signature, key)

    @override
    def __str__(self) -> str:
        return self.sign()
