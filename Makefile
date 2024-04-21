.PHONY: build-backend
build-backend: # Build backend services
	docker build -f ./backend/Dockerfile -t llm-log-parser-backend ./backend

.PHONY: build-frontend
build-frontend: # Build frontend services
	docker build -f ./frontend/Dockerfile -t llm-log-parser-frontend ./frontend

.PHONY: up-dev # Run all services
up-dev: build-backend build-frontend
	docker-compose up
