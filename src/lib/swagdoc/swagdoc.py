from enum import Enum


class SwagMethod(Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


class SwagParam:

    def __init__(
        self,
        name: str,
        location: str,
        type_: str,
        required: bool,
        desc: str,
        default: str,
    ) -> None:
        self.__name: str = name
        self.__location: str = location
        self.__type: str = type_
        self.__required: bool = required
        self.__desc: str = desc
        self.__default: str = default

    @property
    def name(self) -> str:
        return self.__name

    @property
    def location(self) -> str:
        return self.__location

    @property
    def type(self) -> str:
        return self.__type

    @property
    def required(self) -> bool:
        return self.__required

    @property
    def desc(self) -> str:
        return self.__desc

    @property
    def default(self) -> str:
        return self.__default

    def to_doc(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "in": self.location,
            "type": self.type,
            "required": self.required,
            "description": self.desc,
            "default": self.default,
        }


class SwagResp:

    def __init__(self, code: int, desc: str) -> None:
        self.__code: int = code
        self.__desc: str = desc

    @property
    def code(self) -> int:
        return self.__code

    @property
    def desc(self) -> str:
        return self.__desc

    def to_doc(self) -> dict[str, str | int]:
        return {
            "code": self.code,
            "description": self.desc,
        }


class SwagDoc:

    def __init__(
        self,
        path: str,
        method: SwagMethod,
        tags: list[str],
        summary: str,
        params: list[SwagParam],
        resp: list[SwagResp],
    ) -> None:
        self.__path: str = path
        self.__method: SwagMethod = method
        self.__tags: list[str] = tags
        self.__summary: str = summary
        self.__params: list[SwagParam] = params
        self.__resp: list[SwagResp] = resp

    @property
    def path(self) -> str:
        return self.__path

    @property
    def method(self) -> SwagMethod:
        return self.__method

    @property
    def tags(self) -> list[str]:
        return self.__tags

    @property
    def summary(self) -> str:
        return self.__summary

    @property
    def params(self) -> list[SwagParam]:
        return self.__params

    @property
    def resp(self) -> list[SwagResp]:
        return self.__resp

    def to_doc(self):
        return {
            f"{self.method.value}": {
                "tags": self.tags,
                "summary": self.summary,
                "parameters": [param.to_doc() for param in self.params],
                "responses": [res.to_doc() for res in self.resp],
            }
        }
