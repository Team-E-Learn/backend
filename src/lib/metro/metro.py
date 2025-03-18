from typing import Callable, TypeVar

from lib.metro.event import Event

T = TypeVar("T", bound=Event)


class MetroBus:

    _instance: "MetroBus | None" = None

    def __new__(cls) -> "MetroBus":
        if cls._instance is None:
            cls._instance = super(MetroBus, cls).__new__(cls)
            cls._instance.__init()
        return cls._instance

    def __init(self) -> None:
        self.__subscriptions: dict[type[Event], list[Callable[[Event], None]]] = {}

    def publish(self, event: Event) -> Event:
        try:
            for callback in self.__subscriptions[type(event)]:
                callback(event)
        except KeyError as e:
            return event
        return event

    def subscribe(self, obj: type[T], callback: Callable[[T], None]) -> None:
        if obj not in self.__subscriptions.keys():
            self.__subscriptions[obj] = []
        self.__subscriptions[obj].append(callback)
