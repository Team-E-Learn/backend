from enum import Enum
from typing import TypeAlias


class SwagMethod(Enum):
    """
    An enum representing the different HTTP methods and their Swagger
    representation
    """

    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


class SwagParam:
    SwagParamType: TypeAlias = dict[str, str | bool]
    """
    A class that stores a Swagger parameter

    Attributes
    ----------
    name : str
        the name of the parameter.
    location : str
        where the parameter is from.
    type_ : str
        the type of data stored.
    required : bool
        if the data is required or not.
    desc : str
        a description about the data.
    default : str
        the default value of the data.

    Methods
    -------
    to_doc(): SwagParamDoc
        returns the JSON format for the swagger parameter.
    """

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

    def to_doc(self) -> SwagParamType:
        return {
            "name": self.name,
            "in": self.location,
            "type": self.type,
            "required": self.required,
            "description": self.desc,
            "default": self.default,
        }


class SwagResp:
    SwagRespType: TypeAlias = dict[str, str | int]
    """
    A class that stores a Swagger response.

    Attributes
    ----------
    code : int
        stores the associated http status code
    desc : str
        stores description of what the code means relative to the end-point

    Methods
    -------
    to_doc(): dict[str, str | int]
        returns the JSON format for the swagger parameter.
    """

    def __init__(self, code: int, desc: str) -> None:
        self.__code: int = code
        self.__desc: str = desc

    @property
    def code(self) -> int:
        return self.__code

    @property
    def desc(self) -> str:
        return self.__desc

    def to_doc(self) -> SwagRespType:
        return {
            "code": self.code,
            "description": self.desc,
        }


class SwagDoc:
    SwagDocTypes: TypeAlias = (
        list[str] | str | list[SwagParam.SwagParamType] | list[SwagResp.SwagRespType]
    )
    SwagDocType: TypeAlias = dict[
        str, SwagDocTypes
    ]  # used to avoid massive type declarations
    """
    A class that stores the full swagger documentation for an end-point.

    Attributes
    ----------
    method : SwagMethod
        an enum value for the HTTP method type.
    tags : list[str]
        a list of strings for the tags related to the end-point.
    summary : str
        a summary explaining the end-point.
    params : list[SwagParam]
        a list of SwagParams that the end-point takes.
    resp : list[SwagResp]
        a list of SwagResps that the end-point has.

    Methods
    -------
    to_doc(): dict[str, str | int]
        returns the JSON format for the swagger parameter.
    """

    def __init__(
        self,
        method: SwagMethod,
        tags: list[str],
        summary: str,
        params: list[SwagParam],
        resp: list[SwagResp],
    ) -> None:
        self.__method: SwagMethod = method
        self.__tags: list[str] = tags
        self.__summary: str = summary
        self.__params: list[SwagParam] = params
        self.__resp: list[SwagResp] = resp

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

    def to_doc(self) -> SwagDocType:
        return {
            "tags": self.tags,
            "summary": self.summary,
            "parameters": [param.to_doc() for param in self.params],
            "responses": [res.to_doc() for res in self.resp],
        }
