# server_io.py

import asyncio
import websockets
import json

# Example data stored on the server
data = {
    'message': 'Initial data'
}

# List to store WebSocket connections
connections = set()

# WebSocket server handler
async def handle(websocket, path):
    print("Client connected")
    connections.add(websocket)  # Add WebSocket connection to the list
    try:
        # Send initial data to client upon connection
        await websocket.send(json.dumps(data))

        # Keep connection alive to receive updates
        async for message in websocket:
            pass
    finally:
        connections.remove(websocket)  # Remove WebSocket connection from the list
        print("Client disconnected")

async def handle_update_data(websocket, path):
    try:
        async for message in websocket:
            new_data = json.loads(message)
            await update_data(new_data)
    except websockets.exceptions.ConnectionClosedError:
        print("Client connection closed unexpectedly")

# Function to broadcast updates to all connected clients
async def broadcast_update(update):
    tasks = [asyncio.create_task(ws.send(json.dumps(update))) for ws in connections]
    await asyncio.wait(tasks)


# Example function to update data and trigger broadcast
async def update_data(new_data):
    global data
    data = new_data
    print(data)
    await broadcast_update(data)  # Trigger broadcast with updated data

if __name__ == "__main__":  
    start_server = websockets.serve(handle, "localhost", 5000)
    start_update_data_server = websockets.serve(handle_update_data, "localhost", 5001)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_until_complete(start_update_data_server)
    asyncio.get_event_loop().run_forever()
