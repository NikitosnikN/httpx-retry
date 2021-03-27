import logging
import typing
from abc import ABC, abstractmethod

__all__ = ["BaseRetryOptions"]


class BaseRetryOptions(ABC):
    def __init__(
            self,
            attemps: int = 3,
            *,
            exceptions: typing.Optional[typing.Iterable[typing.Type[Exception]]] = None,
            statuses: typing.Optional[typing.Iterable[int]] = None,
            raise_for_status: bool = True,
            logger: logging.Logger = None
    ):
        self.current_attempt = 0
        self.attemps = attemps
        self.exceptions = exceptions or ()
        self.statuses = statuses or ()
        self.raise_for_status = raise_for_status
        self.logger = logger or logging.Logger("httpx-retry")

    @abstractmethod
    def get_sleep_time(self) -> int:
        pass
