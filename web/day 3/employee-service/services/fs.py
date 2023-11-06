
import requests

class FileManager:
    fs_url = 'http://localhost:5002/api/files/'

    def __init__(self) -> None:
        pass

    def create(self, file_path, id):
        conn = requests.post(
                                self.fs_url, 
                                files={'file': open(file_path, 'rb')},
                                data = {'file_id': id})
        return conn.raw
    
    def fetch(self, id):
        conn = requests.get('{}{}'.format(self.fs_url, id))
        return conn.text
    