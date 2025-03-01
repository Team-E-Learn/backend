from abc import ABC, abstractmethod
from typing import override

from werkzeug.wrappers import Response


class IMiddleware(ABC):

    @abstractmethod
    def process(self, response: Response) -> Response:
        pass


class CORSMiddleware(IMiddleware):

    @override
    def process(self, response: Response) -> Response:
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization"
        )
        return response
