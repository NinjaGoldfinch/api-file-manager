# API File manager
A simple file manager that supports HTTPS and websocket connections to interact with a server's filesytem

# Usage
Best way to implement into an existing project is to download:
HTTPS: `file_upload_manager.py` - Uses requests  pip module
Websocket: `file_upload_ws.py` - Uses websockets pip module

## Docker
Recommened deployment with volumes setup to allow for isolated file management
`docker build . -t "File-manager"`
`docker run -d --name "api-file-manager" "File-manager"`

## Python (Not recommended)
Can also be deployed using Python **(ENV recommened!)**
`python3 -m venv .venv`
`source .venv/bin/activate`
`pip3 install -r requirements.txt`
`python3 -u main.py`