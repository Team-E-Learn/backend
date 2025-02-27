from collections.abc import Callable
from flask.app import Flask
from flask_restful import Api, Resource
from werkzeug.wrappers import Response

from lib.swagdoc.swagmanager import SwagManager
from lib.swagdoc.swagtag import SwagTag


class Front:

    def __init__(self, app_name: str) -> None:
        self.__app: Flask = Flask(app_name)
        self.__api: Api = Api(self.__app)
        self.__swag: SwagManager = SwagManager(
            self.__app,
            "Python TSE backend API",
            "Examples of how to use the projects python API",
            "0.0.0",
        )
        self.__after_req: Callable[[Response], Response] | None = None

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

    def add_after_request(self, fun: Callable[[Response], Response]) -> None:
        self.__after_req = fun

    def start(self) -> None:
        self.__swag.start_swag()

        if self.__after_req is not None:
            _ = self.__app.after_request(self.__after_req)

    def run(self) -> None:
        self.__app.run("0.0.0.0")
