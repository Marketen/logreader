import docker
import time
import json

client = docker.from_env()

def read_logs():
    containers = client.containers.list()
    for container in containers:
        if container.name != "log-reader":
            logs = container.logs(tail=20).decode('utf-8')
            with open(f"/logs/{container.name}.log", "w") as f:
                f.write(logs)

while True:
    read_logs()
    time.sleep(60)  # every 1m