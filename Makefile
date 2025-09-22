.PHONY: help build up down logs clean install dev test

# Default target
help:
	@echo "Available commands:"
	@echo "  build     - Build Docker images"
	@echo "  up        - Start services with Docker Compose"
	@echo "  down      - Stop services"
	@echo "  logs      - View logs"
	@echo "  clean     - Clean up containers and images"
	@echo "  install   - Install dependencies locally"
	@echo "  dev       - Start development servers locally"
	@echo "  test      - Run tests"

# Docker commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v --rmi all --remove-orphans

# Local development commands
install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && pnpm install

dev-backend:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

dev-frontend:
	cd frontend && pnpm dev

dev:
	@echo "Starting development servers..."
	@echo "Backend will be available at http://localhost:8000"
	@echo "Frontend will be available at http://localhost:3000"
	@echo "Run 'make dev-backend' and 'make dev-frontend' in separate terminals"

test:
	@echo "Running backend tests..."
	cd backend && python -m pytest
	@echo "Running frontend tests..."
	cd frontend && pnpm test

# Production build
build-prod:
	cd frontend && pnpm build
	docker-compose -f docker-compose.prod.yml build

deploy-prod:
	docker-compose -f docker-compose.prod.yml up -d
