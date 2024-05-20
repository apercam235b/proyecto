import asyncio
import websockets

async def listen():
    uri = "ws://172.24.1.200/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")

asyncio.run(listen())
