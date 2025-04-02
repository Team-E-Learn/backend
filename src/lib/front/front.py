from flask.app import Flask
from flask_restful import Api, Resource
from werkzeug.wrappers import Response

from lib.front.middleware import IMiddleware
from lib.swagdoc.swagmanager import SwagManager
from lib.swagdoc.swagtag import SwagTag

from re import sub


class Front:
    """
    Front is a Facade for both Flask, FlaskRESTful, and SwagDoc. It wraps them
    and allows for easier handling of their functionalities without messing
    around with all the different bits they have.
    """

    __ROUTE_PATTERN: str = (
        r"<([a-z]*):([a-z_]*)>"  # Pattern that converts a Flask route into a swagdoc route.
    )

    def __init__(
        self, app_name: str, doc_title: str, doc_desc: str, version: str
    ) -> None:
        """
        Constructor for Front that sets up Flask, FlaskRESTful Api, and SwagManager.
        """
        self.__app: Flask = Flask(app_name)
        self.__api: Api = Api(self.__app)
        self.__swag: SwagManager = SwagManager(self.__app, doc_title, doc_desc, version)
        self.__middleware: set[IMiddleware] = (
            set()
        )  # Create a set of after request 'middleware' objects

    def register(self, res: type[Resource], route: str, docs: bool = True) -> None:
        """
        Registers a new route.
        """
        self.__api.add_resource(res, route)
        if docs:  # if documentation is enabled on the route
            # get the Swagger style route path
            swag_route: str = sub(Front.__ROUTE_PATTERN, r"{\2}", route)
            self.__swag.add_swag(res, swag_route)

    def add_tag(self, swag_tag: SwagTag) -> None:
        """
        Adds a tag to the SwagManager managed by Front.
        """
        self.__swag.add_tag(swag_tag)

    def add_middleware(self, middleware: IMiddleware) -> None:
        """
        Adds a middleware object to the registry
        """
        self.__middleware.add(middleware)

    def start(self, debug: bool = False) -> None:
        """
        Starts all the required parts for Front to function.
        """
        if debug:  # Don't want documentation in production!
            self.__swag.start_swag()

        if len(self.__middleware) > 0:
            self.__apply_middleware()  # Applies all available middleware

        self.__app.run("0.0.0.0")

    def get_test_client(self):
        """Returns the Flask test client for testing purposes"""
        return self.__app.test_client()

    def __apply_middleware(self) -> None:
        """
        Allows for the middleware to be ran.
        """

        def __run_middleware(resp: Response) -> Response:
            """
            Function defined to act as a "decorated" function which is what
            App.after_request was originally intended for.
            Ensures that each middleware object is used.
            """
            for middle in self.__middleware:
                resp = middle.process(resp)
            return resp

        _ = self.__app.after_request(
            __run_middleware
        )  # Applies all middleware using after_request
