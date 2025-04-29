from abc import ABC, abstractmethod
from typing import override

from werkzeug.wrappers import Response

class IRequestMiddleware(ABC):
    """
    Interface for request Middleware to extend.
    """

    @abstractmethod
    def abort_code(self) -> int:
        pass

    @abstractmethod
    def process(self) -> bool:
        """
        Called when processing is required to happen on the middleware,
        all middleware instances will override this method to handle the Response
        object.
        It returns a boolean represent if the request should be handled (True)
        or dropped (False).
        """
        pass

class IResponseMiddleware(ABC):
    """
    Interface for response Middleware to extend.
    """

    @abstractmethod
    def process(self, response: Response) -> Response:
        """
        Called when processing is required to happen on the middleware,
        all middleware instances will override this method to handle the Response
        object.
        """
        pass


class CORSResponseMiddleware(IResponseMiddleware):
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
        return response
