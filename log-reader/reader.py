import docker
import time
import json
from datetime import datetime

# Initialize Docker client from environment
client = docker.from_env()

def read_logs():
    print(f"[{datetime.now()}] Starting log collection...")
    containers = client.containers.list()

    for container in containers:
        if container.name != "log-reader":
            print(f"[{datetime.now()}] Collecting logs from container: {container.name} (ID: {container.short_id})")
            try:
                logs = container.logs(tail=20).decode('utf-8')
                log_path = f"/logs/{container.name}.log"
                with open(log_path, "w") as f:
                    f.write(logs)
                print(f"[{datetime.now()}] Logs written to {log_path}")
            except Exception as e:
                print(f"[{datetime.now()}] Error reading logs from {container.name}: {e}")

    print(f"[{datetime.now()}] Log collection complete.\n")

# Poll logs every minute
while True:
    read_logs()
    time.sleep(60)
