import socket
from multiprocessing import Process

from pyngrok import ngrok
from pyngrok.conf import get_default
from pyngrok.exception import PyngrokError

from config import logger, settings

get_default().config_path = 'ngrok.yaml'
ngrok.set_auth_token(settings.ngrok_token) if settings.ngrok_token else None


def ngrok_connection():
    try:
        # Open a ngrok tunnel to the socket
        endpoint = ngrok.connect(settings.port.real, "http",
                                 options={"remote_addr": f"{settings.host}:{settings.port.real}"})
        return endpoint.public_url.replace('http://', 'https://')
    except PyngrokError as err:
        logger.error(err)


class Tunnel(Process):
    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.open = False

    def run(self) -> None:
        self._start_tunnel()

    def _start_tunnel(self) -> None:
        self.socket.listen(1)
        connection = None
        try:
            self.open = True
            connection, client_address = self.socket.accept()
        except KeyboardInterrupt:
            logger.info('Tunneling interrupted.')
            if connection:
                connection.close()
            logger.info("Socket connection closed.")
        ngrok.kill(pyngrok_config=None)  # uses default config when None is passed
        self.socket.close()
        self.open = False

    def kill(self) -> None:
        if self.open:
            logger.info("Resetting ngrok config.")
            ngrok.kill(pyngrok_config=None)
            logger.info("Closing socket connection.")
            self.socket.close()
