v ?=
export NONE_DOCKER_IMAGES := $(shell docker images -f dangling=true -q)

guard-v:
	@if [ -z "$(v)" ]; then \
		echo "v is required. Example: make bs v=qiskit0200"; \
		exit 1; \
	fi

QISKIT0_SERVICES := qiskit0201 qiskit0211 qiskit0212 qiskit0222 qiskit0223 qiskit0232 qiskit0240
QISKIT1_SERVICES := qiskit100 qiskit102 qiskit110 qiskit120 qiskit124 qiskit131 qiskit132
QISKIT2_SERVICES := qiskit200 qiskit202 qiskit211 qiskit221 qiskit223 qiskit230 qiskit231

b: ## build all images
	docker compose build --no-cache

b0: ## build services using Dockerfile.qiskit0
	docker compose build --no-cache $(QISKIT0_SERVICES)

b1: ## build services using Dockerfile.qiskit1
	docker compose build --no-cache $(QISKIT1_SERVICES)

b2: ## build services using Dockerfile.qiskit2
	docker compose build --no-cache $(QISKIT2_SERVICES)

bs: guard-v ## build one (usage: make bs v=qiskit0200)
	docker compose build --no-cache $(v)

u: ## up all containers
	docker compose up -d

us: guard-v ## up one (usage: make us v=qiskit0200)
	docker compose up -d $(v)

c: guard-v ## connect (usage: make c v=qiskit0200)
	docker compose exec $(v) bash

uc: guard-v ## up and connect (usage: make uc v=qiskit0200)
	docker compose up -d $(v)
	docker compose exec $(v) bash

d: ## down all containers
	docker compose down

rmi-none: ## remove dangling images
	@if [ -n "$(NONE_DOCKER_IMAGES)" ]; then docker rmi $(NONE_DOCKER_IMAGES) -f; fi

clean-v: guard-v ## remove one service container and local image
	docker compose down $(v) --rmi local -v --remove-orphans || true

clean-all: ## remove everything possible for disk space
	docker compose down --rmi all -v --remove-orphans || true
	@if [ -n "$$(docker ps -aq)" ]; then docker rm -f $$(docker ps -aq); fi
	@if [ -n "$$(docker images -aq)" ]; then docker rmi -f $$(docker images -aq); fi
	@if [ -n "$$(docker volume ls -q)" ]; then docker volume rm -f $$(docker volume ls -q); fi
	@if [ -n "$$(docker network ls --filter type=custom -q)" ]; then docker network rm $$(docker network ls --filter type=custom -q) || true; fi
	docker builder prune -a -f
	docker system prune -a -f --volumes

help: ## this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'