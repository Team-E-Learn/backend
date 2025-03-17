from abc import ABC, abstractmethod
from typing import LiteralString, override

from psycopg.connection import Connection
from psycopg.cursor import Cursor
from psycopg.rows import TupleRow

from lib.dataswap.result import AllowedParams, SwapResult, PsqlResult
from lib.dataswap.statement import IStatement


class SwapCursor(ABC):

    @abstractmethod
    def execute(
        self, statement: IStatement, params: AllowedParams = None
    ) -> SwapResult:
        pass


class PsqlCursor(SwapCursor):

    def __init__(self, conn: Connection[TupleRow]):
        self.__conn: Connection[TupleRow] = conn

    @override
    def execute(
        self, statement: IStatement, params: AllowedParams = None
    ) -> PsqlResult:
        query: LiteralString = statement.to_string()
        cursor: Cursor[TupleRow] = self.__conn.cursor().execute(query, params)
        return PsqlResult(cursor)
