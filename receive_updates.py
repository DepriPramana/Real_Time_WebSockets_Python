# receive_updates.py
import asyncio
import websockets
import time

async def receive_updates():
    uri = "ws://localhost:5000"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to WebSocket server")
                while True:
                    message = await websocket.recv()
                    print("Received data update:", message)
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed unexpectedly: {e}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)
        except ConnectionRefusedError as e:
            print("Failed to connect to the server:", e)
            print("Exiting...")
            break

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(receive_updates())
