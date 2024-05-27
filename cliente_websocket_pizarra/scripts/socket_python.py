import asyncio
import websockets
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')logger = logging.getLogger(__name__)

async def handle_client(websocket, path):
    async for message in websocket:
        logger.info(f"Received: {message}")
        if message == "1":
            logger.info("Ejecutando script pizarra 1")
            response = "Hemos hecho una foto de la pizarra 1"
        elif message == "2":
            logger.info("Ejecutando script pizarra 2")
            response = "Hemos hecho una foto de la pizarra 2"
        else:
            logger.info(f"Received unknown state: {message}")
            response = "No tengo almacenado este estado"
        await websocket.send(response)

async def main():
    server = await websockets.serve(handle_client, "localhost", 8766)
    logger.info("Server started and listening on ws://localhost:8766")
    await server.wait_closed()

# Punto de entrada del script
if __name__ == "__main__":
    asyncio.run(main())