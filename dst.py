import docker
import json
import time
import os

path = os.environ.get("DST_PATH", "/data/status.json")
interval = int(os.environ.get("DST_INTERVAL", "30"))
filter_label = os.environ.get("DST_FILTER_LABEL", False)
filters = {}
if filter_label:
    filters["label"] = filter_label
name_label = os.environ.get("DST_NAME_LABEL", False)
url_label = os.environ.get("DST_URL_LABEL", False)

client = docker.from_env()

def formatContainer(container):
    state = container.attrs.get("State", {})
    health = state.get("Health", {})
    return {
        "name": container.labels.get(name_label, container.name),
        "url": container.labels.get(url_label),
        "status": container.status,
        "start": state.get("StartedAt"),
        "stop": state.get("FinishedAt"),
        "health": {
            "status": health.get("Status", "none"),
            "fails": health.get("FailingStreak", 0)
        }
    }

def loop():
    while True:
        try:
            report = list(
                map(formatContainer,
                    client.containers.list(all=True, filters=filters)))
            with open(path, 'w') as outfile:
                json.dump(report, outfile)
        except docker.errors.NotFound:
            print('Container bad move. Restarting.')
        time.sleep(interval)

try:
    loop()
except KeyboardInterrupt:
    print('\n\nKeyboard exception received. Exiting.')
    exit()