from abc import ABC


class Event(ABC):
    pass


class CancellableEvent(Event):

    def __init__(self) -> None:
        self.__cancelled: bool = False

    @property
    def cancelled(self) -> bool:
        return self.__cancelled

    @cancelled.setter
    def cancelled(self, value: bool) -> None:
        self.__cancelled = value

    def cancel(self) -> None:
        self.cancelled = True

    def toggle(self) -> None:
        self.cancelled = not self.cancelled
