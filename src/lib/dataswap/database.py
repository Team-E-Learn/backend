from abc import ABC, abstractmethod
from typing import override

from psycopg import connect as psql_connect
from psycopg.connection import Connection
from psycopg.rows import TupleRow

from lib.dataswap.cursor import SwapCursor, PsqlCursor


class SwapDB(ABC):

    def __init__(self, conn_info: str) -> None:
        self._conn_info: str = conn_info

    @abstractmethod
    def get_cursor(self) -> SwapCursor:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass


class PsqlDatabase(SwapDB):

    def __init__(self, conn_info: str) -> None:
        super().__init__(conn_info)
        self.__conn: Connection[TupleRow] = psql_connect(self._conn_info)

    @override
    def get_cursor(self) -> PsqlCursor:
        return PsqlCursor(self.__conn)

    @override
    def commit(self) -> None:
        self.__conn.commit()
