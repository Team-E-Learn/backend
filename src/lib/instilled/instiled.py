from typing import Callable, TypeVar

T = TypeVar("T")


class Instil[T]:
    """
    A class that allows it to be used as a function decorator to inject
    objects (services) into classes that are not being instantiated by
    ourselves.

    Attributes
    ----------
    service_name : str
        stores the name of the service that is intended for use.

    Methods
    -------
    add_service(cls, service_name: str, obj: object):
        a class method used to add a service that can be found with @Instil.
    """

    __services: dict[str, object] = {}  # registry of services

    def __init__(self, service_name: str) -> None:
        self.__service_name: str = service_name

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        def instil_wrapper(*args, **kwargs) -> T:
            if self.__service_name not in Instil.__services.keys():
                raise InstilException  # service does not exist
            return func(*args, **kwargs, service=Instil.__services[self.__service_name])

        return instil_wrapper

    @classmethod
    def add_service(cls, service_name: str, obj: object) -> None:
        """
        A class method that is used to append items into the static __services
        attribute of the class.

        Parameters
        ----------
        service_name : str
            the name that will be associated with the obj param.
        obj : object
            the object (service) that will be used when requested by a
            function decorated with @Instil("service_name")
        """
        cls.__services[service_name] = obj


class InstilException(Exception):
    """
    An extremely basic implementation of a python exception used to signify if
    a function was incorrectly using @Instil and did not apply a service by the
    given name.
    """

    pass
