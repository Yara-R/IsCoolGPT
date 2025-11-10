.PHONY: help install test test-cov test-unit test-integration lint format clean docker-build docker-up docker-down docker-logs

# Cores para output
BLUE=\033[0;34m
GREEN=\033[0;32m
RED=\033[0;31m
NC=\033[0m # No Color

help: ## Mostra esta mensagem de ajuda
	@echo "$(BLUE)Assistente Educacional - Comandos Disponíveis$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# Instalação
install: ## Instala dependências
	@echo "$(BLUE)Instalando dependências...$(NC)"
	pip install -r requirements.txt
	pip install -r requirements-test.txt

install-dev: install ## Instala dependências de desenvolvimento
	@echo "$(GREEN)Dependências instaladas!$(NC)"

# Testes
test: ## Executa todos os testes
	@echo "$(BLUE)Executando testes...$(NC)"
	pytest tests/ -v

test-cov: ## Executa testes com cobertura
	@echo "$(BLUE)Executando testes com cobertura...$(NC)"
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term

test-unit: ## Executa apenas testes unitários
	@echo "$(BLUE)Executando testes unitários...$(NC)"
	pytest tests/ -v -m unit

test-integration: ## Executa apenas testes de integração
	@echo "$(BLUE)Executando testes de integração...$(NC)"
	pytest tests/ -v -m integration

test-watch: ## Executa testes em modo watch
	@echo "$(BLUE)Executando testes em modo watch...$(NC)"
	pytest-watch tests/ -v

# Qualidade de código
lint: ## Verifica qualidade do código
	@echo "$(BLUE)Verificando código com flake8...$(NC)"
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format: ## Formata código com black
	@echo "$(BLUE)Formatando código...$(NC)"
	black . --line-length=100
	@echo "$(GREEN)Código formatado!$(NC)"

type-check: ## Verifica tipos com mypy
	@echo "$(BLUE)Verificando tipos...$(NC)"
	mypy . --ignore-missing-imports

# Docker
docker-build: ## Constrói imagens Docker
	@echo "$(BLUE)Construindo imagens Docker...$(NC)"
	docker-compose build
	@echo "$(GREEN)Build concluído!$(NC)"

docker-up: ## Inicia containers
	@echo "$(BLUE)Iniciando containers...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Containers iniciados!$(NC)"
	@echo "Frontend: http://localhost"
	@echo "API: http://localhost:8000/docs"

docker-down: ## Para containers
	@echo "$(BLUE)Parando containers...$(NC)"
	docker-compose down
	@echo "$(GREEN)Containers parados!$(NC)"

docker-logs: ## Mostra logs dos containers
	docker-compose logs -f

docker-restart: docker-down docker-up ## Reinicia containers

docker-clean: ## Remove containers, volumes e imagens
	@echo "$(RED)Limpando Docker...$(NC)"
	docker-compose down -v --rmi all
	@echo "$(GREEN)Limpeza concluída!$(NC)"

# Desenvolvimento
dev: ## Inicia servidor de desenvolvimento
	@echo "$(BLUE)Iniciando servidor de desenvolvimento...$(NC)"
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-test: ## Inicia com hot-reload para testes
	@echo "$(BLUE)Modo desenvolvimento com testes...$(NC)"
	pytest-watch tests/ -v &
	uvicorn main:app --reload

# Limpeza
clean: ## Remove arquivos temporários
	@echo "$(BLUE)Limpando arquivos temporários...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml
	@echo "$(GREEN)Limpeza concluída!$(NC)"

clean-all: clean docker-clean ## Remove tudo (arquivos temporários + Docker)

# Verificações
check: lint type-check test ## Executa todas as verificações
	@echo "$(GREEN)Todas as verificações passaram!$(NC)"

ci: check ## Simula pipeline de CI
	@echo "$(GREEN)Pipeline CI concluído com sucesso!$(NC)"

# Deployment
deploy-build: ## Build para produção
	@echo "$(BLUE)Build de produção...$(NC)"
	docker-compose -f docker-compose.yml build --no-cache
	@echo "$(GREEN)Build de produção concluído!$(NC)"

deploy-up: ## Deploy em produção
	@echo "$(BLUE)Iniciando deploy...$(NC)"
	docker-compose -f docker-compose.yml up -d
	@echo "$(GREEN)Deploy concluído!$(NC)"

# Utilitários
health: ## Verifica saúde da API
	@echo "$(BLUE)Verificando saúde da API...$(NC)"
	@curl -s http://localhost:8000/health | python -m json.tool || echo "$(RED)API não está respondendo$(NC)"

logs-api: ## Mostra logs da API
	docker-compose logs -f api

logs-frontend: ## Mostra logs do frontend
	docker-compose logs -f frontend

shell-api: ## Abre shell no container da API
	docker-compose exec api /bin/bash

# Coverage
coverage-report: ## Abre relatório de cobertura
	@echo "$(BLUE)Abrindo relatório de cobertura...$(NC)"
	python -m webbrowser htmlcov/index.html || open htmlcov/index.html || xdg-open htmlcov/index.html

# Informações
info: ## Mostra informações do sistema
	@echo "$(BLUE)Informações do Sistema$(NC)"
	@echo ""
	@echo "Python: $$(python --version)"
	@echo "Docker: $$(docker --version)"
	@echo "Docker Compose: $$(docker-compose --version)"
	@echo ""
	@echo "Status dos containers:"
	@docker-compose ps || echo "Containers não iniciados"