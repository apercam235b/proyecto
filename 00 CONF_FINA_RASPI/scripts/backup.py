import asyncio
import websockets
import logging
import os
from servo import posicion1, posicion2

# Configuración del logging
logging.basicConfig(level=logging.INFO,filename='log.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def handle_client(websocket, path):
    async for message in websocket:
        logger.info(f"Received: {message}")
        if message == "1":
                logger.info("Ejecutando script pizarra 1")
                response = "Hemos hecho una foto de la pizarra 1"
                posicion1()
        elif message == "2":
                logger.info("Ejecutando script pizarra 2")
                response = "Hemos hecho una foto de la pizarra 2"
                posicion2()
        elif message == "3":
                logger.info("Ejecutando script de empezar grabacion")
        #Aqui la funcion de empezar a grabar
                response = "Se ha iniciado la grabacion"
        elif message == "4":
                logger.info("Se ha detenido la grabacion")
                response = "Termina la grabacion"
        elif message == "5":
                logger.info("Tomando una foto")
                os.system("touch /datos/clase1/hola.png")
                response = "Se ha tomado una foto"
        elif message == "6":
                logger.info("Inicia la clase")
                os.system("mkdir -p /datos/clase1")
                response = "se ha iniciado la clase"
        elif message == "7":
                logger.info("Finaliza la clase")
                response = "Finaliza la clase"
		break
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
