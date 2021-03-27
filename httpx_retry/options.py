import logging
import random
import typing

__all__ = ["ConstantRetry", "RandomRetry", "IncrementalRetry", "ExponentialRetry"]

from .base import BaseRetryOptions


class ConstantRetry(BaseRetryOptions):
    def __init__(
            self,
            attemps: int = 3,
            timeout: int = 3,
            *,
            exceptions: typing.Optional[typing.Iterable[typing.Type[Exception]]] = None,
            statuses: typing.Optional[typing.Iterable[int]] = None,
            raise_for_status: bool = True,
            logger: logging.Logger = None
    ):
        super().__init__(
            attemps=attemps,
            exceptions=exceptions,
            statuses=statuses,
            raise_for_status=raise_for_status,
            logger=logger
        )
        self._timeout = timeout

    def get_sleep_time(self, **kwargs) -> int:
        return self._timeout


class RandomRetry(BaseRetryOptions):
    def __init__(
            self,
            attemps: int = 3,
            min_timeout: int = 1,
            max_timeout: int = 10,
            *,
            exceptions: typing.Optional[typing.Iterable[typing.Type[Exception]]] = None,
            statuses: typing.Optional[typing.Iterable[int]] = None,
            raise_for_status: bool = True,
            logger: logging.Logger = None
    ):
        super().__init__(
            attemps=attemps,
            exceptions=exceptions,
            statuses=statuses,
            raise_for_status=raise_for_status,
            logger=logger
        )
        self._min_timeout = min_timeout
        self._max_timeout = max_timeout

    def get_sleep_time(self, **kwargs) -> int:
        return random.randint(self._min_timeout, self._max_timeout)


class IncrementalRetry(BaseRetryOptions):
    def __init__(
            self,
            attemps: int = 3,
            start_timeout: int = 1,
            max_timeout: int = 10,
            factor: int = 1,
            *,
            exceptions: typing.Optional[typing.Iterable[typing.Type[Exception]]] = None,
            statuses: typing.Optional[typing.Iterable[int]] = None,
            raise_for_status: bool = True,
            logger: logging.Logger = None
    ):
        super().__init__(
            attemps=attemps,
            exceptions=exceptions,
            statuses=statuses,
            raise_for_status=raise_for_status,
            logger=logger
        )
        self._start_timeout = self._next_timeout = start_timeout
        self._max_timeout = max_timeout
        self._factor = factor

    def get_sleep_time(self) -> int:
        timeout = self._start_timeout + (self._factor * self.current_attempt)
        return min(timeout, self._max_timeout)


class ExponentialRetry(BaseRetryOptions):
    def __init__(
            self,
            attemps: int = 3,
            start_timeout: int = 1,
            max_timeout: int = 10,
            factor: int = 2,
            *,
            exceptions: typing.Optional[typing.Iterable[typing.Type[Exception]]] = None,
            statuses: typing.Optional[typing.Iterable[int]] = None,
            raise_for_status: bool = True,
            logger: logging.Logger = None
    ):
        super().__init__(
            attemps=attemps,
            exceptions=exceptions,
            statuses=statuses,
            raise_for_status=raise_for_status,
            logger=logger
        )
        self._start_timeout = self._next_timeout = start_timeout
        self._max_timeout = max_timeout
        self._factor = factor

    def get_sleep_time(self) -> int:
        timeout = self._start_timeout * (self._factor ** self.current_attempt)
        return min(timeout, self._max_timeout)
