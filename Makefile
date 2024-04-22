.PHONY: build-backend
build-backend: # Build backend services
	docker build -f ./backend/Dockerfile -t fact-extractor-backend ./backend

.PHONY: build-frontend
build-frontend: # Build frontend services
	docker build -f ./frontend/Dockerfile -t fact-extractor-frontend ./frontend

.PHONY: up-dev # Run all services
up-dev: build-backend build-frontend
	docker-compose up
