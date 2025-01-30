from typing import Callable, TypeVar

T = TypeVar("T")


class Instil[T]:
    __services: dict[str, object] = {}

    def __init__(self, service_name: str) -> None:
        self.__service_name: str = service_name

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        def instil_wrapper(*args, **kwargs) -> T:
            if self.__service_name not in Instil.__services.keys():
                raise InstilException
            return func(*args, **kwargs, service=Instil.__services[self.__service_name])
        return instil_wrapper

    @classmethod
    def add_service(cls, service_name: str, obj: object) -> None:
        cls.__services[service_name] = obj


class InstilException(Exception):
    pass
