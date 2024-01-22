import abc
import aiohttp
from aiohttp import ClientTimeout


class AbstractRestRequest(abc.ABC):
    GET = "GET"

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError


class AsyncRestRequest(AbstractRestRequest):

    def __init__(self, service_name, method, url):
        self.service_name = service_name
        self.method = method
        self.url = url

    async def run(self):
        method = None
        if self.method == self.GET:
            method = self.get
        return await method()

    async def get(self):
        return await self._request_get()

    async def _request_get(self):
        async with aiohttp.request(
            method=self.GET,
            url=self.url,
        ) as responce:
            answer = await responce.json(content_type=None)
            return answer

