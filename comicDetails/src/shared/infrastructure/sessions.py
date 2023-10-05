from aiohttp import ClientSession, ClientTimeout, TCPConnector

from .settings import get_settings

settings = get_settings()


class GeneralSession:
    """
    Class used to manage the aiohttp sessions to be used in the microservice.

    Attributes:
        session: client session generated for requests
    """
    async def client(self):
        """ Create a client session for aiohttp """
        session = ClientSession(
            timeout=ClientTimeout(connect=int(settings.HTTP_TIMEOUT_SEC)),
            connector=TCPConnector(ssl=True, limit=3)
        )
        return session
