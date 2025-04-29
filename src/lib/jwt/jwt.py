from base64 import urlsafe_b64decode, urlsafe_b64encode
from hashlib import sha256
import hmac
from json import dumps, loads
from typing import TypeAlias, override

ALLOWED_CLAIM_DATA: TypeAlias = str | int

def _hash_msg(msg: bytes, key: bytes) -> str:
    hash_: bytes = hmac.new(key=key, msg=msg, digestmod=sha256).digest()
    return urlsafe_b64encode(hash_).decode().strip("=")


def _encode(string: str) -> str:
    return urlsafe_b64encode(bytes(string, "latin-1")).decode().strip("=")

class JwtValidator:
    def __init__(self, header: str, payload: str, signature: str, key: bytes) -> None:
        self.__header: str = header
        self.__payload: str = payload
        self.__signature: str = signature
        self.__key: bytes = key

    def get_header(self) -> dict[str, ALLOWED_CLAIM_DATA]:
        return loads(urlsafe_b64decode(self.__header).decode())

    def get_payload(self) -> dict[str, ALLOWED_CLAIM_DATA]:
        return loads(urlsafe_b64decode(self.__payload).decode())

    @staticmethod
    def validate(header: str, payload: str, signature: str, key: bytes) -> bool:
        msg: bytes = bytes(f"{header}.{payload}", "latin-1")
        return _hash_msg(msg, key) == signature


    @staticmethod
    def str_load(token: str, key: bytes) -> "JwtValidator | None":
        if token.count(".") != 2:
            return None 
        
        header, payload, signature = token.split(".")

        if not JwtValidator.validate(header, payload, signature, key):
            return None

        return JwtValidator(header, payload, signature, key)


class Jwt:

    def __init__(self, key: bytes) -> None:
        self.__key: bytes = key
        self.__claims: dict[str, ALLOWED_CLAIM_DATA] = {}

    def add_claim(self, name: str, value: ALLOWED_CLAIM_DATA) -> "Jwt":
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

    @override
    def __str__(self) -> str:
        return self.sign()

def test_jwt() -> None:
    VALID_JWT: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJpc3N1ZXItbmFtZSJ9.7NH2e1OCKoRHIpiCKIhSxSqrpPR5o245fIxcVnAMeEs"
    VALID_KEY: bytes = b"secretkeysecretkeysecretkeysecretkey"
    # valid key confirmed via https://jwt.io/

    valid_jwt: str = Jwt(VALID_KEY) \
        .add_claim("iss", "issuer-name") \
        .sign()

    assert valid_jwt == VALID_JWT, "Failed check against valid token"
    
    invalid_key_jwt: str = Jwt(b"wrongkey") \
        .add_claim("iss", "issuer-name") \
        .sign()
    
    assert invalid_key_jwt != VALID_JWT, "Failed check against invalid token key"
    
    invalid_claim_jwt: str = Jwt(b"secretkeysecretkeysecretkeysecretkey") \
        .add_claim("iss", "wrong-name") \
        .sign()
    
    assert invalid_claim_jwt != VALID_JWT, "Failed check against invalid token claim"


    validator: JwtValidator | None = JwtValidator.str_load(VALID_JWT, VALID_KEY)
    assert validator is not None, "Validator failed to load valid token"
    assert validator.get_payload()["iss"] == "issuer-name", "Invalid issuer from payload"
    
    
    print(f">> Test passed for JWT library")


if __name__ == "__main__":
    test_jwt()
