from flask.app import Flask
from flask_restful import Api, Resource
from werkzeug.wrappers import Response

from lib.front.middleware import IMiddleware
from lib.swagdoc.swagmanager import SwagManager
from lib.swagdoc.swagtag import SwagTag

from re import sub


class Front:
    __ROUTE_PATTERN: str = r"<([a-z]*):([a-z_]*)>"

    def __init__(self, app_name: str) -> None:
        self.__app: Flask = Flask(app_name)
        self.__api: Api = Api(self.__app)
        self.__swag: SwagManager = SwagManager(
            self.__app,
            "Python TSE backend API",
            "Examples of how to use the projects python API",
            "0.0.0",
        )
        self.__middleware: list[IMiddleware] = []

    def register(self, res: type[Resource], route: str, swag: bool = True) -> None:
        self.__api.add_resource(res, route)
        if swag:
            swag_route: str = sub(Front.__ROUTE_PATTERN, r"{\2}", route)
            self.__swag.add_swag(res, swag_route)

    def add_tag(self, swag_tag: SwagTag) -> None:
        self.__swag.add_tag(swag_tag)

    def add_middleware(self, middleware: IMiddleware) -> None:
        self.__middleware.append(middleware)

    def run(self, debug: bool = False) -> None:
        if debug:
            self.__swag.start_swag()

        if len(self.__middleware) > 0:
            self.__apply_middleware()

        self.__app.run("0.0.0.0")

    def __apply_middleware(self) -> None:
        def __run_middleware(resp: Response) -> Response:
            for middle in self.__middleware:
                resp = middle.process(resp)
            return resp

        _ = self.__app.after_request(__run_middleware)
