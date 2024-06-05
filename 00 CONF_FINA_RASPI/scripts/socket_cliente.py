import asyncio
import websockets
import logging
import os
import requests
from servo import posicion1, posicion2

# Configuración del logging
logging.basicConfig(level=logging.INFO, filename='log.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

base_url='http://localhost:5080'

async def handle_client(websocket, path):
    is_running = True
    while is_running:
        message = await websocket.recv()  # Espera un mensaje
        logger.info(f"Recibido: {message}")
        if message == "1":
            url = f"{base_url}/log"
            log_message = "Moviendo servo a pizarra 1"
            logger.info(log_message)
            data = {"message": log_message}
            requests.post(url, json=data)

            logger.info("Ejecutando script de pizarra 1")
            response = "Se ha tomado una foto de la pizarra 1"
            posicion1()
        elif message == "2":
            url = f"{base_url}/log"
            log_message = "Moviendo servo a pizarra 2"
            logger.info(log_message)
            data = {"message": log_message}
            requests.post(url, json=data)

            logger.info("Ejecutando script de pizarra 2")
            response = "Se ha tomado una foto de la pizarra 2"
            posicion2()
        elif message == "3":
            url = f"{base_url}/log"
            log_message = "Se ha iniciado la grabacion"
            logger.info(log_message)
            data = {"message": log_message}
            requests.post(url, json=data)

            logger.info("Ejecutando script para empezar grabación")
            response = "Se ha iniciado la grabación"
        elif message == "4":
            url = f"{base_url}/log"
            log_message = "Se ha detenido la grabacion"
            logger.info(log_message)
            data = {"message": log_message}
            requests.post(url, json=data)

            logger.info("Deteniendo la grabación")
            response = "Se ha detenido la grabación"

        elif message == "5":
            url = f"{base_url}/log"
            log_message = "Se ha tomado una foto"
            logger.info(log_message)
            data = {"message": log_message}
            requests.post(url, json=data)
            os.system("touch /datos/clase1/hola.png")
            response = "Se ha tomado una foto"

        elif message == "6":
            url = f"{base_url}/log"
            log_message = "Iniciando la clase"
            logger.info(log_message)
            data = {"message": log_message}
            requests.post(url, json=data)

            os.system("mkdir -p /datos/clase1")
            response = "Se ha iniciado la clase"

        elif message == "7":
            url = f"{base_url}/log"
            log_message = "Termina la clase"
            logger.info(log_message)
            data = {"message": log_message}
            requests.post(url, json=data)

            logger.info("Finalizando la clase")
            response = "Se ha finalizado la clase"
            #is_running = False
            #await websocket.close()
        else:
            logger.info(f"Estado desconocido recibido: {message}")
            response = "No reconozco este estado"
        await websocket.send(response)

async def main():
    server = await websockets.serve(handle_client, "localhost", 8766)
    logger.info("Server started and listening on ws://localhost:8766")
    await server.wait_closed()

# Punto de entrada del script
if __name__ == "__main__":
    asyncio.run(main())
