from abc import ABC, abstractmethod
from typing import override

from werkzeug.wrappers import Response


class IMiddleware(ABC):
    """
    Interface for Middleware to extend.
    """

    @abstractmethod
    def process(self, response: Response) -> Response:
        """
        Called when processing is required to happen on the middleware,
        all middleware instances will extend this method to handle the Response
        object.
        """
        pass


class CORSMiddleware(IMiddleware):
    """
    The CORSMiddleware object has been created to solve issues relating
    to CORS parameters not existing inside of the response to incoming
    requests.
    """

    @override
    def process(self, response: Response) -> Response:
        """
        Applies the necessary headers for CORS to function correctly.
        """
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization"
        )
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        return response
