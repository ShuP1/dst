import docker
import json
import time
import os

title = os.environ.get("DST_TITLE", "Docker Status")
caption = os.environ.get("DST_CAPTION", 'Status page using <a href="https://git.wadza.fr/me/dst">dst</a>')
path = os.environ.get("DST_PATH", "/data")
interval = int(os.environ.get("DST_INTERVAL", "30"))
filter_label = os.environ.get("DST_FILTER_LABEL", False)
filters = {}
if filter_label:
    filters["label"] = filter_label
name_label = os.environ.get("DST_NAME_LABEL", False)
url_label = os.environ.get("DST_URL_LABEL", False)

css = 'body{padding:0;max-width:50em;margin:auto;background:#f2f2f2;box-shadow:0 0.5rem 1rem rgba(0, 0, 0, 0.2);font-family:-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"}.content{background:#fcfcfc;padding:1rem;text-align:center}footer,header{text-align:center}section{margin:1rem;border:1px #eee solid;border-radius:4px;background:white;display:flex;padding:0.5rem 1rem}section *{margin:0}h2{flex-grow:1;text-align:left}h2 a{text-decoration:none}section p{align-self:center}.health,.status{text-transform:capitalize;min-width:5em}.health::after,.status::after{font-size:1.5rem;vertical-align:middle}.health-none,.status-created,.status-paused{color:cornflowerblue}.health-healthy,.status-running{color:#7ED321}.health-healthy::after,.status-running::after{content:"\\2714"}.health-starting,.status-removing,.status-restarting{color:#ffbf00}.health-starting::after,.status-restarting::after{content:"\\21bb"}.status-removing::after{content:"\\21af"}.health-unhealthy,.status-dead,.status-exited{color:orangered}.health-unhealthy::after,.status-dead::after,.status-exited::after{content:"\\2718"}a{color:black}'
header = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{0}</title><link rel="stylesheet" href="style.css"></head><body><div class="content"><header><h1>{0}</h1><h5>{1}</h5></header>'
section = '<section><h2><a href="{1}">{0}</a></h2><p class="status status-{2}" title="{3}">{2}</p><p class="health health-{4}" title="{5}">{4}</p></section>'
footer = '<footer><a href="https://git.wadza.fr/me/dst">Docker Status</a></footer></div></body></html>'

client = docker.from_env()

def formatContainer(container):
    state = container.attrs.get("State", {})
    health = state.get("Health", {})
    return {
        "name": container.labels.get(name_label, container.name),
        "url": container.labels.get(url_label, ""),
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

            with open(path + "/style.css", 'w') as outfile:
                outfile.write(css)

            with open(path + "/status.json", 'w') as outfile:
                json.dump(report, outfile)

            with open(path + "/index.html", 'w') as outfile:
                outfile.write(header.format(title, caption))
                for l in report:
                    outfile.write(
                        section.format(
                            l.get("name"), l.get("url"), l.get("status"),
                            l.get("stop") if l.get("status") in ["exited", "dead"] else l.get("start"),
                            l.get("health").get("status"), l.get("health").get("fails")))
                outfile.write(footer)

        except docker.errors.NotFound:
            print('Container bad move. Restarting.')
        time.sleep(interval)

try:
    loop()
except KeyboardInterrupt:
    print('\n\nKeyboard exception received. Exiting.')
    exit()