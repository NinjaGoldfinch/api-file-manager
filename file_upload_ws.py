import asyncio
import time
import websockets
import json

async def send_and_receive(websocket, json_data):
    # Send a message to the server
    try: data = json.dumps(json_data)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return
    await websocket.send(data)
    print("Message sent to the server")

    # Receive a message from the server
    response = await websocket.recv()
    print(f"Message received from the server: {response}")

async def list_files(websocket):
    await send_and_receive(websocket, {'action': 'list_files'})

async def upload_file(websocket, filename, file_content):
    if isinstance(file_content, dict):
        file_content = json.dumps(file_content)
    await send_and_receive(websocket, {'action': 'upload_file', 'filename': filename, 'file_content': file_content})

async def download_file(websocket, filename):
    await send_and_receive(websocket, {'action': 'download_file', 'filename': filename})
    


async def communicate_with_wss():
    uri = "ws://localhost:8000/ws"  # Replace with your WSS server URI
    async with websockets.connect(uri) as websocket:
        while True:
            await list_files(websocket)
            await download_file(websocket, "hello.txtas")
            await upload_file(websocket, "foo.json", {"success": "true"})
            time.sleep(1)

# Run the WebSocket client
if __name__ == "__main__":
    asyncio.run(communicate_with_wss())