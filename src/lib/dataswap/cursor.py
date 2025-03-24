from abc import ABC, abstractmethod
from typing import LiteralString, override

from psycopg.connection import Connection
from psycopg.cursor import Cursor
from psycopg.rows import TupleRow

from lib.dataswap.result import AllowedParams, SwapResult, PsqlResult
from lib.dataswap.statement import IStatement


class SwapCursor(ABC):
    """
    The abstract implementation for a cursor object for databases
    """

    @abstractmethod
    def execute(
        self, statement: IStatement, params: AllowedParams = None
    ) -> SwapResult:
        """
        Execute a passed statement and return the query object
        """
        pass


class PsqlCursor(SwapCursor):

    def __init__(self, conn: Connection[TupleRow]):
        self.__conn: Connection[TupleRow] = conn

    @override
    def execute(
        self, statement: IStatement, params: AllowedParams = None
    ) -> PsqlResult:
        query: LiteralString = (
            statement.to_string()
        )  # convert the statement to a string
        cursor: Cursor[TupleRow] = self.__conn.cursor().execute(
            query, params
        )  # run the query with psql
        return PsqlResult(cursor)
