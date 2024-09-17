from json import JSONDecodeError

from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute
from starlette.responses import JSONResponse, FileResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

import os
import uvicorn

from functions.file_functions import *

DOCKER_CONTAINER = os.getenv('DOCKER_CONTAINER', 'false')

if DOCKER_CONTAINER == 'true':
    BASE_DIR = '/files'
else:
    BASE_DIR = "SET_YOUR_BASE_DIR_HERE"

# Route functions

# TODO: Add permissions to routes (using API keys) to allow for creation of directories, deletion of files, etc.
# Also assign different permissions to different API keys, which allows each service to access different files / directories
# And prevents certain services from deleting / creating files etc.

# LATER: Also allow for access to an SQL database, which will allow for easier data management and querying
# This will speed up the process of finding files, and allow for more complex queries to be run on the data
# Might archive this repository and create a new one for the SQL database, as it will be a vastly different project

async def get_files(request):
    directory = BASE_DIR
    
    files = list_files(directory)
    if not files:
        return JSONResponse({'success': False,'error': 'Directory not found'}, status_code=404)
    
    return JSONResponse(files)

async def get_file(request):
    filename = request.path_params['filename']
    file_path = os.path.join(BASE_DIR, filename)
    
    file = download_file(file_path)
    
    if file.get('error'):
        return JSONResponse(file, status_code=404)
    
    return FileResponse(file)
    

async def send_file(request):
    print("Received a file upload request")
    form = await request.form()

    files_written = await upload_file(form, BASE_DIR)

    return JSONResponse({'success': True, 'files_written': files_written})

async def delete_file(request):
    filenames = request.query_params.getlist('filenames')
    
    removed_files = remove_file(BASE_DIR, filenames)
    
    if 'error' in removed_files:
        return JSONResponse(removed_files, status_code=400)
    
    return JSONResponse(removed_files)

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            
            action = data.get('action')

            if action == 'list_files':
                directory = BASE_DIR
                
                if not os.path.exists(directory) or not os.path.isdir(directory):
                    await websocket.send_json({'error': 'Directory not found'})
                    continue

                files = []
                for root, dirs, filenames in os.walk(directory):
                    for dirname in dirs:
                        dir_path = os.path.join(root, dirname)
                        file_count = sum([len(files) for r, d, files in os.walk(dir_path)])
                        files.append({'name': dirname, 'type': 'directory', 'file_count': file_count})
                    for filename in filenames:
                        file_path = os.path.join(root, filename)
                        files.append({'name': filename, 'type': 'file'})
                    break  # Only process the top-level directory

                await websocket.send_json({'success': 'true', 'files': files})
                

            elif action == 'download_file':
                filename = data.get('filename')
                file_path = os.path.join(BASE_DIR, filename)
                
                if os.path.exists(file_path):
                    if os.path.isdir(file_path):
                        await websocket.send_json({'error': 'Requested path is a directory'})
                        continue
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                    await websocket.send_bytes(file_data)
                else:
                    await websocket.send_json({'error': 'File not found'})

            elif action == 'upload_file':
                filename = data.get('filename')
                file_content = data.get('file_content')
                if not filename or not file_content:
                    await websocket.send_json({'error': 'Filename and file content are required'})
                    continue

                file_path = os.path.join(BASE_DIR, filename)
                with open(file_path, 'wb') as f:
                    f.write(file_content.encode('utf-8'))
                await websocket.send_json({'success': 'true', 'file_written': filename})

            else:
                print("Invalid action")
                await websocket.send_json({'error': 'Invalid action'})
    
    except JSONDecodeError:
        print("JSONDecodeError")
        await websocket.send_json({'error': 'Invalid JSON data'})
        
    except WebSocketDisconnect:
        return
    
    except Exception as e:
        print(f"An error occurred: {e}")
        await websocket.send_json({'error': 'An error occurred'})

routes = [
    Route('/files', get_files),
    Route('/files/{filename}', get_file),
    Route('/upload', send_file, methods=['POST']),
    Route('/delete', delete_file, methods=['DELETE']),
    WebSocketRoute('/ws', websocket_endpoint)
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)