# Makefile for managing Airflow Docker Compose setup

# Colors for help message
RED=\033[31m
GREEN=\033[32m
YELLOW=\033[33m
RESET=\033[0m
# Default target
.PHONY: help

help:  ## Show this help message
	@echo -e "$(GREEN)Available Commands:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-15s$(RESET) %s\n", $$1, $$2}'

Initialize:
	docker compose up airflow-init

up: ## Start all services in detached mode
	docker compose up -d

down: ## Stop and remove all services, volumes, and images
	docker compose down --volumes --rmi all

restart: ## Restart all Airflow services
	docker compose restart

restart_only:
	docker compose restart airflow-scheduler airflow-webserver

init: ## Initialize the Airflow database (run only once or after reset)
	docker compose up airflow-init

logs: ## Tail logs from all running containers
	docker compose logs -f

ps: ## List running containers
	docker ps

bash-webserver: ## Open a bash shell in the Airflow webserver container
	docker exec -it $(shell docker ps -qf "name=airflow-webserver") /bin/bash

bash-scheduler: ## Open a bash shell in the Airflow scheduler container
	docker exec -it $(shell docker ps -qf "name=airflow-scheduler") /bin/bash

# copy-config: ## Copy airflow.cfg from container to local config directory
# 	## Since we already changed this config in our docker_compose.yaml file, we don't need this command anymore.
# 	docker cp $(shell docker ps -qf "name=airflow-webserver"):/opt/airflow/airflow.cfg ./config/airflow.cfg

build: ## Build the Docker images (required after modifying Dockerfile)
	docker compose build

prune: ## Clean up unused Docker resources (dangling images, stopped containers)
	docker system prune -f

upgrade: ## Upgrade Airflow database schema after Airflow version update
	docker compose run airflow-worker airflow db upgrade

tail-log-file: ## Tail the output_log.txt from the logs directory
	#tail -f ./logs/output_log.txt
	tail -f ./dags/output_log.txt

clean: ## Remove DAG logs and output files
	rm -rf ./logs/* #./config/airflow.cfg

force-clean: ## Force remove all containers and images
	docker stop $(shell docker ps -aq) || true
	docker rm -f $(shell docker ps -aq) || true
	docker rmi -f $(shell docker images -aq) || true
	docker volume rm $(shell docker volume ls -q) || true
	docker system prune -a --volumes -f

