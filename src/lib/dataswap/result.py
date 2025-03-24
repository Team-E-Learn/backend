from abc import ABC, abstractmethod
from typing import Any, TypeAlias, override

from psycopg.cursor import Cursor
from psycopg.rows import TupleRow

AllowedResults: TypeAlias = str | int | float | bool
AllowedParams: TypeAlias = tuple[AllowedResults, ...] | None


class SwapResult(ABC):
    """
    An abstract implementation for a database result object.
    """

    @abstractmethod
    def fetch_one(self) -> tuple[Any, ...] | None:
        """
        Converts the result object into a tuple.
        """
        pass

    @abstractmethod
    def fetch_all(self) -> list[tuple[Any, ...]] | None:
        """
        Converts the result object into a list of tuples.
        """
        pass


class PsqlResult(SwapResult):

    def __init__(self, result: Cursor[TupleRow]) -> None:
        self.__result: Cursor[TupleRow] = result

    @override
    def fetch_one(self) -> tuple[Any, ...] | None:
        return self.__result.fetchone()

    @override
    def fetch_all(self) -> list[tuple[Any, ...]] | None:
        return self.__result.fetchall()
