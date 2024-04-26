import yaml
import shutil
import os
import schedule
from os import path
from loguru import logger
from device import Device
import requests
import json
import time

class Exporter:
    def __init__(self):
        self.devices = []
        self.report_interval = int(os.getenv("REPORT_INTERVAL"))
        self.tb_server_address= os.getenv("TB_SERVER_ADDRESS")
        self.config_path = 'config/devices.yaml'
        self.load_devices()
        

    def load_devices(self):
        try:
            logger.info("Loading devices list")
            if not path.exists(self.config_path):
                shutil.copy('devices.yaml', self.config_path)
            with open("config/devices.yaml",'r',encoding='utf-8') as stream:
                try:
                    for _device in yaml.safe_load(stream)["devices"]:
                        self.devices.append(Device(ip=_device["ip"],username=_device["username"],password=_device["password"],access_token=_device["access_token"]))
                except yaml.YAMLError as exc:
                    logger.error(exc)
        except Exception as e:
            logger.error(str(e))
            
            
    def report(self):
        headers = {"Content-Type": "application/json"}
        
        for device in self.devices:
            report_url = f"{self.tb_server_address}/api/v1/{device.access_token}/telemetry" 
            device.login()
            status = device.getStatus()
            payload = {
                "state":device.getPower(),
                "Total Energy":status.get('StatusSNS').get('ENERGY').get('Total',''),
                "Yesterday Energy":status.get('StatusSNS').get('ENERGY').get('Yesterday'),
                "Today Energy":status.get('StatusSNS').get('ENERGY').get('Today'),
                "Voltage":status.get('StatusSNS').get('ENERGY').get('Voltage'),
                "Current":status.get('StatusSNS').get('ENERGY').get('Current')
            }
            
            try:
                response = requests.post(report_url, headers=headers, data=json.dumps(payload))
                response.raise_for_status()  # Raise an exception for HTTP errors (non-2xx responses)
                print(f"Data sent successfully for {device.getFriendlyName()}" )
            except requests.exceptions.RequestException as e:
                print(f"Failed to send data: {e}")
                
                

if __name__ == "__main__":
    exporter = Exporter()
    exporter.report()
    schedule.every(10).minutes.do(exporter.report)
    
    while True:
        schedule.run_pending()
        time.sleep(1)