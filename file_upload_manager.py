import requests

import json

class FileUploadManager:
    def __init__(self, url: str) -> None:
        self.url = url
        self.filesToUpload = []
        
    def addFile(self, filename: str, content) -> None:
        self.filesToUpload.append((filename, content))
        
    def uploadFiles(self) -> None:
        files = {}
        
        for filename, content in self.filesToUpload:
            if isinstance(content, str):
                files[filename] = (filename, content)
            elif isinstance(content, dict):
                files[filename] = (filename, json.dumps(content))
        
        print(files)
        
        response = requests.post(self.url, files=files)
        
        if response.status_code == 200:
            print(response.json())
        else:
            print("Failed to upload files")
    
    def uploadFile(self, filename: str, content) -> None:
        files = {}
        
        if isinstance(content, str):
            files[filename] = (filename, content)
        elif isinstance(content, dict):
            files[filename] = (filename, json.dumps(content))
        
        response = requests.post(self.url, files=files)
        
        if response.status_code == 200:
            print(response.json())
        else:
            print("Failed to upload file")

# Usage
if __name__ == '__main__':
    print("Testing started")
    file_upload_manager = FileUploadManager('http://localhost:8000/upload')
    file_upload_manager.addFile('hello.txt', 'This is the content of the file.')
    file_upload_manager.addFile('world.json', {'success': 'true'})
    file_upload_manager.uploadFiles()
    file_upload_manager.uploadFile('blah.txt', 'Random stuff!')