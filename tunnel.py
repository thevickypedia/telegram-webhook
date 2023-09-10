import socket

from pyngrok import ngrok
from pyngrok.conf import get_default
from pyngrok.exception import PyngrokError

from config import logger, settings

get_default().config_path = 'ngrok.yaml'
ngrok.set_auth_token(settings.ngrok_token)


def tunnel() -> None:
    try:
        # Open a ngrok tunnel to the socket
        endpoint = ngrok.connect(settings.port, "http", options={"remote_addr": f"{settings.host}:{settings.port}"})
        public_url = endpoint.public_url.replace('http://', 'https://')
    except PyngrokError as err:
        logger.error(err)
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.listen(1)
    connection = None

    logger.warning(f'http://{settings.host}:{settings.port} -> {public_url}')
    try:
        connection, client_address = sock.accept()
    except KeyboardInterrupt:
        logger.warning('\nInterrupted manually.')
        if connection:
            connection.close()
        logger.warning("Connection closed.")
    ngrok.kill(pyngrok_config=None)  # uses default config when None is passed
    sock.close()


if __name__ == '__main__':
    tunnel()
