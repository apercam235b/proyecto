import asyncio
import websockets
import re
import logging
import asyncio
import websockets
import re
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def listen():
    uri = "ws://192.168.1.200/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            logger.info(f"Received: {message}")
            # Eliminar todos los caracteres que no sean números
            numeric_message = re.sub(r'\D', '', message)
            if numeric_message == "5":
                logger.info("ID es 5, Mandando opción de apuntar pizarra 1")
                await mandar_mensaje("1")
            elif numeric_message == "6":
                logger.info("ID es 6, Mandando opción de apuntar pizarra 2")
                await mandar_mensaje("2")
            elif numeric_message == "7":
                logger.info("ID es 7, Empieza la grabacion de la pizarra")
                await mandar_mensaje("3")
            elif numeric_message == "8":
                logger.info("ID es 8, Termina la grabacion")
                await mandar_mensaje("4")
            elif numeric_message == "9":
                logger.info("ID es 9, Tomando una foto...")
                await mandar_mensaje("5")
            elif numeric_message == "10":
                logger.info("ID es 10, Inicia la clase")
                await mandar_mensaje("6")
            elif numeric_message == "11":
                logger.info("ID es 11, finaliza la clase")
                await mandar_mensaje("7")


async def mandar_mensaje(message):
    uri = "ws://localhost:8766"
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        logger.info(f"Response from other client: {response}")

# Punto de entrada del script
if __name__ == "__main__":
    asyncio.run(listen())
