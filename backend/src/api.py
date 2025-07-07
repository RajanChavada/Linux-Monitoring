"""
    Module for fastAPI endpoints to retrieve system information.
"""


from fastapi import FastAPI 
from monitor.system_info import SystemInfo

app = FastAPI(title="System Metrics API", version="1.0")

monitor = SystemInfo()

@app.get("/metrics")
def get_metrics(): 
    return monitor.collect_all()



