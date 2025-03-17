from abc import ABC, abstractmethod
from typing import LiteralString, override


class IStatement(ABC):

    @abstractmethod
    def to_string(self) -> LiteralString:
        pass


class StringStatement(IStatement):

    def __init__(self, statement: LiteralString) -> None:
        self.__statement: LiteralString = statement

    @override
    def to_string(self) -> LiteralString:
        return self.__statement
