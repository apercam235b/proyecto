import asyncio
import websockets
import re

async def listen():
    uri = "ws://172.24.1.200/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")
            # Eliminar todos los caracteres que no sean números
            numeric_message = re.sub(r'\D', '', message)
            if numeric_message == "5":
                print("toma una foto")

asyncio.run(listen())
