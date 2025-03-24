from enum import Enum
from typing import override
from lib.metro.event import Event


class LogLevel(Enum):
    LOG = 0
    WARN = 1
    ERROR = 2


class LogEvent(Event):

    def __init__(self, level: LogLevel, message: str) -> None:
        self.__level: LogLevel = level
        self.__message: str = message

    @property
    def message(self) -> str:
        return self.__message

    @property
    def level(self) -> LogLevel:
        return self.__level

    @override
    def __str__(self) -> str:
        return f"[{self.level.name}] {self.message}"
