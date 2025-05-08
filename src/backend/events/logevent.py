from enum import Enum
from typing import override
from lib.metro.event import Event


class LogLevel(Enum):
    """
    An enum that represents the 3 varieties of log levels that can occur.
    """

    LOG = 0
    WARN = 1
    ERROR = 2


class LogEvent(Event):
    """
    A basic event that handles passing log messages to an event handler for
    further processing, helping to abstract away irrelevant logging
    functionalities.

    This has more usages than just printing an error log, for example one
    listener could do the printing and another may count the errors and send
    them to a dashboard or into an email report.
    """

    def __init__(self, level: LogLevel, message: str) -> None:
        self.__level: LogLevel = level  # The log severity level
        self.__message: str = message  # The message associated

    @property
    def message(self) -> str:
        """
        A property decorated method to get the message.
        """
        return self.__message

    @property
    def level(self) -> LogLevel:
        """
        A property decorated method to get the log level.
        """
        return self.__level

    @override
    def __str__(self) -> str:
        """
        Converts the event into a message that can be displayed out.
        """
        return f"[{self.level.name}] {self.message}"
