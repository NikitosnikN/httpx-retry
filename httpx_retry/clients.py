import asyncio
import time
import typing

from httpx import Client, AsyncClient, Response

from .base import BaseRetryOptions
from .options import *


# TODO solve issue with coping code (cause of sleep and request) for both sync and async clients,
# maybe move logic to retry options instance

class RetryClient(Client):
    def __init__(
            self,
            retry_options: BaseRetryOptions = ConstantRetry(),
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._retry_options = retry_options

    def request(
            self,
            *args,
            **kwargs,
    ) -> typing.Optional[Response]:
        self._retry_options.current_attempt += 1

        try:
            response = super().request(*args, **kwargs)

            if response.status_code in self._retry_options.statuses:
                if self._retry_options.current_attempt < self._retry_options.attemps:
                    time.sleep(self._retry_options.get_sleep_time())
                    return self.request(*args, **kwargs)

                elif self._retry_options.raise_for_status:
                    response.raise_for_status()

            return response

        except Exception as e:
            if self._retry_options.current_attempt < self._retry_options.attemps:
                for _exception in self._retry_options.exceptions:
                    if isinstance(e, _exception):
                        time.sleep(self._retry_options.get_sleep_time())
                        return self.request(*args, **kwargs)

            raise e


class AsyncRetryClient(AsyncClient):
    def __init__(
            self,
            retry_options: BaseRetryOptions = ConstantRetry(),
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._retry_options = retry_options

    async def request(
            self,
            *args,
            **kwargs,
    ) -> Response:
        self._retry_options.current_attempt += 1

        try:
            response = await super().request(*args, **kwargs)

            if response.status_code in self._retry_options.statuses:
                if self._retry_options.current_attempt < self._retry_options.attemps:
                    await asyncio.sleep(self._retry_options.get_sleep_time())
                    return await self.request(*args, **kwargs)

                elif self._retry_options.raise_for_status:
                    response.raise_for_status()

            return response

        except Exception as e:
            if self._retry_options.current_attempt < self._retry_options.attemps:
                for _exception in self._retry_options.exceptions:
                    if isinstance(e, _exception):
                        await asyncio.sleep(self._retry_options.get_sleep_time())
                        return await self.request(*args, **kwargs)

            raise e
