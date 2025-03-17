from abc import ABC, abstractmethod
from typing import Any, TypeAlias, override

from psycopg.cursor import Cursor
from psycopg.rows import TupleRow

AllowedResults: TypeAlias = str | int | float | bool
AllowedParams: TypeAlias = tuple[AllowedResults, ...] | None


class SwapResult(ABC):

    @abstractmethod
    def fetch_one(self) -> tuple[Any, ...] | None:
        pass

    @abstractmethod
    def fetch_all(self) -> list[tuple[Any, ...]] | None:
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
