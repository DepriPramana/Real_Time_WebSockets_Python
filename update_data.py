# update_data.py
import asyncio
import websockets
import json

async def update_data(new_data):
    uri = "ws://localhost:5001/update_data"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(new_data))
        print("Sent updated data to server")

if __name__ == "__main__":
    new_data = {"message": "New updated data"}
    asyncio.get_event_loop().run_until_complete(update_data(new_data))
