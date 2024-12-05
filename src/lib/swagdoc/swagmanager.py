from collections.abc import Callable
from typing import TypeVar
from flasgger import Swagger
from flask import Flask

from lib.swagdoc.swagdoc import SwagDoc
from lib.swagdoc.swagtag import SwagTag

T = TypeVar("T")

class swag_me:
    def __init__(self, doc: SwagDoc) -> None:
        self.__doc: SwagDoc = doc

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        def swag_wrapper(*args, **kwargs) -> T:
            return func(*args, **kwargs)
        setattr(swag_wrapper, "has_swag", True)
        setattr(swag_wrapper, "swag_doc", self.__doc)
        return swag_wrapper

class SwagManager:

    def __init__(self, app: Flask, title: str, desc: str, version: str) -> None:
        self.__app: Flask = app
        self.__title: str = title
        self.__desc: str = desc
        self.__version: str = version
        self.__tags: list[SwagTag] = []
        self.__docs: list[SwagDoc] = [] 
        self.__swagger: Swagger | None = None

    def start_swag(self) -> None:
        self.__swagger = Swagger(
            self.__app,
            template={
                "info": {
                    "title": self.__title,
                    "description": self.__desc,
                    "version": self.__version,
                },
                "tags": [],
                "paths": {doc.path: doc.to_doc() for doc in self.__docs},
            },
        )

    def add_tag(self, tag: SwagTag) -> None:
        self.__tags.append(tag)
   
    def add_swag(self, cls: type) -> None:
        for item in dir(cls):
            attr: object = getattr(cls, item)
            if not callable(attr):
                continue
            if not getattr(attr, "has_swag", False):
                continue
            docs: SwagDoc | None = getattr(attr, "swag_doc", None)
            if docs is None:
                continue
            self.__docs.append(docs)
