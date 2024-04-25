import os
import requests
from loguru import logger

class Device:
    ip: str
    status:str
    username: str
    password: str
    access_token: str

    
    def __init__(self,ip:str,username: str, password:str, access_token:str, status:str = "off"):
        self.ip = ip
        self.status = status
        self.username = username
        self.password = password
        self.access_token = access_token
        self.url = 'http://' + self.ip
    
    def login(self):
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.auth = self.session.post(self.url)
        return self

    def send_request(self,command:str):
        params = {'cmnd': str(command)}
        with self.session.get(f"{self.url}/cm", params=params) as resp:
            if resp.status_code == 200:
                return resp.json()
            
    def getPower(self):
        response = self.send_request(f'Power')   
        return response.get("POWER","")
    
    def getFriendlyName(self):
        response = self.send_request(f'FriendlyName')
        return response.get("FriendlyName1","")
    
    def getStatus(self):
        response = self.send_request(f'Status 10')
        # logger.warning(response)
        return response