from typing import Callable, TypeVar

from lib.metro.event import Event

T = TypeVar("T", bound=Event)  # Generic type to ensure all passed objects are Events


class MetroBus:
    """
    The MetroBus is a singleton that acts as a simple
    Publisher/Subscriber system so that functions can be created that are
    dynamically called based on Event objects that are passed to the event bus.
    """

    _instance: "MetroBus | None" = (
        None  # Static class member to store the singleton instance.
    )

    def __new__(cls) -> "MetroBus":
        if cls._instance is None:  # If there is no current instance, create one
            cls._instance = super(MetroBus, cls).__new__(
                cls
            )  # Instantiate a new MetroBus
            cls._instance.__init()  # Call the replacement constructor
        return (
            cls._instance
        )  # return the _instance (results in the same object when newly instantiated)

    def __init(self) -> None:
        """
        A replacement for the __init__ method for the singleton class.
        This initialises the empty subscriptions dictionary.
        """
        self.__subscriptions: dict[type[Event], list[Callable[[Event], None]]] = {}

    def publish(self, event: Event) -> Event:
        """
        Publishes an event to be processed by the event bus.
        """
        try:
            for callback in self.__subscriptions[
                type(event)
            ]:  # For each callback related to an event type
                callback(event)  # Call the function and pass the event
        except KeyError as e:  # The event is unused
            return event
        return event

    def subscribe(self, obj: type[T], callback: Callable[[T], None]) -> None:
        """
        Subscribes a function to be called when an event is published.
        """
        if (
            obj not in self.__subscriptions.keys()
        ):  # check if event has been registered before
            self.__subscriptions[obj] = []  # initialise empty list of callbacks
        self.__subscriptions[obj].append(callback)  # add callback to registry


class TestEvent(Event):
    def __init__(self) -> None:
        self.found_event: bool = False

    def set_found(self) -> None:
        self.found_event = True

def test_metro() -> None:
    MetroBus().subscribe(TestEvent, lambda e: e.set_found())

    event: TestEvent = TestEvent()
    _ = MetroBus().publish(event)
    assert event.found_event, "Event successfully modified"
    
    print(f">> Test passed for Metro library")

if __name__ == "__main__":
    test_metro()
