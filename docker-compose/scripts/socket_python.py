import asyncio
import websockets
import re
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def listen():
    uri = "ws://172.24.1.200/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            logger.info(f"Received: {message}")
            # Eliminar todos los caracteres que no sean números
            numeric_message = re.sub(r'\D', '', message)
            if numeric_message == "5":
                logger.info("Taking a photo")

asyncio.run(listen())
