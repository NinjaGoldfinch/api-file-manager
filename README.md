# API File manager
A simple file manager that supports HTTPS and websocket connections to interact with a server's filesytem. This is a super simple file-system manager, and has no complex features like read / write locks etc. Most likely will be archived soon.

# Usage
Best way to implement into an existing project is to download:\
HTTPS: `file_upload_manager.py` - Uses requests  pip module\
Websocket: `file_upload_ws.py` - Uses websockets pip module

## Docker
Recommened deployment with volumes setup to allow for isolated file management\
`docker build . -t "file-manager"`\
`docker run -d -p 8000:8000 --name "api-file-manager" "file-manager"`

Also recommended to implement a volume for data retention:\
`docker volume create "API-data"`\
`docker run -d -p 8000:8000 -v "API-data":/files --name "api-file-manager" "file-manager"`

## Python (Not recommended)
Can also be deployed using Python **(ENV recommened!)**\
`python3 -m venv .venv`\
`source .venv/bin/activate`\
`pip3 install -r requirements.txt`\
`python3 -u main.py`
