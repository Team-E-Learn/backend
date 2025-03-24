from abc import ABC


class Event(ABC):
    """
    Basic interface representing an event
    """

    pass


class CancellableEvent(Event, ABC):
    """
    An extended version of Event that allows for it to be cancelled.
    Although this does not have any functionality in MetroBus to handle this,
    it means that events can be passed to their listeners, cancelled there
    then the calling publisher can check the state and perform actions based on
    this.
    """

    def __init__(self) -> None:
        self.__cancelled: bool = False

    @property
    def cancelled(self) -> bool:
        """
        Property to get the current value of cancelled.
        """
        return self.__cancelled

    @cancelled.setter
    def cancelled(self, value: bool) -> None:
        """
        Setter property to set the value of cancelled.
        """
        self.__cancelled = value

    def cancel(self) -> None:
        """
        Sets cancelled to True.
        """
        self.cancelled = True

    def toggle(self) -> None:
        """
        Toggles cancelled.
        """
        self.cancelled = not self.cancelled
