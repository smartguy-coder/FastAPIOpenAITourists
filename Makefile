DC = docker compose
API_CONTAINER = backend1

.PHONY: up down bash
up:
	${DC} up

down:
	${DC} down

bash:
	${DC} exec -it ${API_CONTAINER} bash
