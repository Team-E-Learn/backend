from collections.abc import Callable
from typing import TypeVar
from flasgger import Swagger
from flask import Flask

from lib.swagdoc.swagdoc import SwagDoc
from lib.swagdoc.swagtag import SwagTag

T = TypeVar("T")


class SwagGen:
    """
    A class that is used as a decorator to find and store SwagDoc objects

    Attributes
    ----------
    doc : SwagDoc
        stores the SwagDoc object for applying to the method
    """

    def __init__(self, doc: SwagDoc) -> None:
        self.__doc: SwagDoc = doc

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        def swag_wrapper(*args, **kwargs) -> T:
            return func(*args, **kwargs)

        setattr(swag_wrapper, "swag_doc", self.__doc)
        return swag_wrapper


class SwagManager:
    """
    A class used to manage Swagger documentation generation.

    Attributes
    ----------
    app : Flask
        a reference to the created Flask app (used to create swagger page).
    title : str
        a title for the API.
    desc : str
        a description for the API.
    version : str
        a version for the API.
    tags : list[SwagTag]
        a list of all tags inside the API.
    docs : dict[str, list[SwagDoc]]
        a dictionary containing all the api endpoints and the documentation.
    swagger : Swagger | None
        a reference to the created swagger object.

    Methods
    -------
    start_swagger():
        creates the swagger object through flasgger.
    add_tag():
        adds a tag to the list of tags.
    add_swag(obj: object, path: str):
        takes in a object and a path and attempts to discover all @SwagGen
        decorators that exist within the class.
    """

    def __init__(self, app: Flask, title: str, desc: str, version: str) -> None:
        self.__app: Flask = app
        self.__title: str = title
        self.__desc: str = desc
        self.__version: str = version
        self.__tags: list[SwagTag] = []
        self.__docs: dict[str, list[SwagDoc]] = {}
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
                "paths": {
                    path: {doc.method.value: doc.to_doc() for doc in docs}
                    for path, docs in self.__docs.items()
                },
            },
        )

    def add_tag(self, tag: SwagTag) -> None:
        self.__tags.append(tag)

    def add_swag(self, obj: object, path: str) -> None:
        if path not in self.__docs:  # ensures key exists
            self.__docs[path] = []

        for item in dir(obj):  # get names of all attributes of the object
            attr: object = getattr(obj, item)  # get object attribute by name
            if not callable(attr):  # checks if the attribute is callable
                continue
            docs: SwagDoc | None = getattr(
                attr, "swag_doc", None
            )  # checks if the attribute has swag_doc (default to None)
            if docs is None:
                continue
            self.__docs[path].append(docs)  # has @SwagGen, add to docs
