IMAGE := bugs4q-plus
CONTAINER := bugs4q-plus
WORKDIR := /src

b: ## build image
	docker build --no-cache -t $(IMAGE) .

u: ## run container
	docker run -d --name $(CONTAINER) -v "$$(pwd):$(WORKDIR)" -w $(WORKDIR) $(IMAGE) sleep infinity

c: ## connect container
	docker exec -it $(CONTAINER) bash

uc: ## run and connect
	docker run --rm -it --name $(CONTAINER) -v "$$(pwd):$(WORKDIR)" -w $(WORKDIR) $(IMAGE) bash

d: ## stop and remove container
	docker rm -f $(CONTAINER) || true

re: d b uc ## rebuild and connect

rmi-none: ## remove dangling images
	@if [ -n "$$(docker images -f dangling=true -q)" ]; then \
		docker rmi -f $$(docker images -f dangling=true -q); \
	fi

clean: d ## remove image and dangling images
	docker rmi -f $(IMAGE) || true
	@if [ -n "$$(docker images -f dangling=true -q)" ]; then \
		docker rmi -f $$(docker images -f dangling=true -q); \
	fi

help: ## this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'