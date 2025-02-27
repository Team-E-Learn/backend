from flask.app import Flask
from flask_restful import Api, Resource

from lib.swagdoc.swagmanager import SwagManager
from lib.swagdoc.swagtag import SwagTag


class Front:

    def __init__(self, app: Flask) -> None:
        self.__app: Flask = app
        self.__api: Api = Api(app)
        self.__swag: SwagManager = SwagManager(
            self.__app,
            "Python TSE backend API",
            "Examples of how to use the projects python API",
            "0.0.0",
        )

    def register(
        self,
        resource: type[Resource],
        route: str,
        swag_route: str,
    ) -> None:
        self.__api.add_resource(resource, route)
        self.__swag.add_swag(resource, swag_route)

    def add_swag_tag(self, swag_tag: SwagTag) -> None:
        self.__swag.add_tag(swag_tag)

    def add_resource(self, resource: type[Resource], route: str) -> None:
        self.__api.add_resource(resource, route)

    def start(self) -> None:
        self.__swag.start_swag()
