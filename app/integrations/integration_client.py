from app.adapters.integration import AsyncRestRequest


class IntegrationClient:

    async def run(
            self,
            service_name,
            method,
            url
    ):
        request_adapter = AsyncRestRequest(
            service_name=service_name,
            method=method,
            url=url
        )

        remote_responce = await request_adapter.run()
        return remote_responce

    async def get_riddle_text(self):
        service_name = 'FastAPI'
        method = 'GET'
        url = 'http://127.0.0.1:8000/riddles'

        answer = await self.run(
            service_name,
            method,
            url
        )
        return answer['body']['data'][0]['question']['text']


