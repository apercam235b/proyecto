import asyncio
import websockets

async def listen():
    uri = "ws://172.24.1.28:80"  # Reemplaza <ESP32_IP> con la dirección IP de tu ESP32

    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server")

        try:
            while True:
                message = await websocket.recv()
                print(f"Received message: {message}")
        except websockets.ConnectionClosed:
            print("Connection closed")

# Ejecuta la función listen
asyncio.get_event_loop().run_until_complete(listen())
