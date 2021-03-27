import time

from httpx import Client, AsyncClient, Response

from .base import BaseRetryOptions
from .options import *


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
    ) -> Response:
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
            if self._retry_options.current_attempt < self._retry_options.attemps \
                    and e in self._retry_options.exceptions:
                time.sleep(self._retry_options.get_sleep_time())
                self.request(*args, **kwargs)

            raise e


class AsyncRetryClient(AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def request(
            self,
            *args,
            **kwargs,
    ) -> Response:
        # TODO
        return await super().request(*args, **kwargs)
