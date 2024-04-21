import asyncio
import websockets

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/000000"  # Address of the FastAPI server
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            print("Received:", response)

# Start the event loop and run the test
asyncio.get_event_loop().run_until_complete(test_websocket())

