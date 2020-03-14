# Docker Status

Simple status page using Docker sdk and healthcheck.

## Options

Environment variable | Description | Default
--- | --- | ---
DOCKER_* | Docker client options | [Doc](https://docker-py.readthedocs.io/en/stable/client.html#docker.client.from_env)
DST_PATH | Files output | `/data`
DST_INTERVAL | Update interval is seconds | `30`
DST_FILTER_LABEL | Filter visible containers with label | `False`
DST_NAME_LABEL | Override container name with label | `False`
DST_URL_LABEL | Provide url with label | `False`
DST_TITLE | Page title | `Docker Status`
DST_CAPTION | Page caption

## TODO

[x] Json periodic static
[ ] Static Front
[ ] Groups
[ ] Events
[ ] Gotify

## Licence
Distributed under the GPL3 license.