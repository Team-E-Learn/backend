from abc import ABC, abstractmethod
from typing import LiteralString, override


class IStatement(ABC):
    """
    Interface for representing a statement.

    This has been written as an interface to support the potential expansion
    into SQL query generators via a 'BuilderStatement' or 'StatementFactory'
    that may be able to product SQL queries instead of being written by hand.
    """

    @abstractmethod
    def to_string(self) -> LiteralString:
        """
        Called to transform a statement into a LiteralString.
        LiteralString is a common string format used for database libraries.
        """
        pass


class StringStatement(IStatement):
    """
    The most basic possible implementation of IStatement, it is used for just
    plain SQL statements.
    """

    def __init__(self, statement: LiteralString) -> None:
        self.__statement: LiteralString = statement

    @override
    def to_string(self) -> LiteralString:
        return self.__statement
