import asyncio
import websockets
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Proxy")

class StratumProxy:
    def __init__(self, listen_host, listen_port, default_pool, default_port):
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.default_pool = default_pool
        self.default_port = default_port

    async def handle_connection(self, websocket, path):
        pool_url = f"ws://{self.default_pool}:{self.default_port}"
        logger.info(f"New worker connected: {path}")

        try:
            async with websockets.connect(pool_url) as pool_websocket:
                worker_to_pool = self.relay(websocket, pool_websocket, "Worker -> Pool")
                pool_to_worker = self.relay(pool_websocket, websocket, "Pool -> Worker")
                await asyncio.gather(worker_to_pool, pool_to_worker)
        except Exception as e:
            logger.error(f"Connection error: {e}")

    async def relay(self, source, destination, direction):
        try:
            async for message in source:
                logger.info(f"{direction}: {message}")
                await destination.send(message)
        except websockets.ConnectionClosed:
            logger.info(f"Connection closed: {direction}")
        except Exception as e:
            logger.error(f"Relay error ({direction}): {e}")

    def start(self):
        logger.info(f"Starting proxy on {self.listen_host}:{self.listen_port}")
        start_server = websockets.serve(self.handle_connection, self.listen_host, self.listen_port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    listen_host = "0.0.0.0"      # Lắng nghe trên tất cả IP
    listen_port = 8080           # Cổng proxy lắng nghe
    default_pool = "minotaurx.na.mine.zpool.ca"  # Pool mặc định
    default_port = 7019          # Cổng pool mặc định

    proxy = StratumProxy(listen_host, listen_port, default_pool, default_port)
    proxy.start()
