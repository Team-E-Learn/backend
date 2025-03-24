from abc import ABC, abstractmethod
from typing import override

from psycopg import connect as psql_connect
from psycopg.connection import Connection
from psycopg.rows import TupleRow

from lib.dataswap.cursor import SwapCursor, PsqlCursor


class SwapDB(ABC):
    """
    The abstract implementation of the swappable database system
    """

    def __init__(self, conn_info: str) -> None:
        self._conn_info: str = conn_info  # Get the connection info to interpret

    @abstractmethod
    def get_cursor(self) -> SwapCursor:
        """
        Get an instance of the SwapCursor for the connection.
        """
        pass

    @abstractmethod
    def commit(self) -> None:
        """
        Commits the current changes to the database
        """
        pass


class PsqlDatabase(SwapDB):
    """
    The PostgreSQL implementation for SwapDB
    """

    def __init__(self, conn_info: str) -> None:
        super().__init__(conn_info)
        # Initialise psql connection
        self.__conn: Connection[TupleRow] = psql_connect(self._conn_info)

    @override
    def get_cursor(self) -> PsqlCursor:
        return PsqlCursor(self.__conn)  # Creates an instance of PsqlCursor

    @override
    def commit(self) -> None:
        self.__conn.commit()
