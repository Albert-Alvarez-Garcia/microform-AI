# Makefile para el proyecto Microform

# Variables
PYTHON = python3
SERVER_FILE = ai_fetcher.py

.PHONY: help install run clean

help: ## Muestra esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instala las dependencias necesarias
	@echo "Instalando dependencias..."
	@$(PYTHON) -m pip install -r requirements.txt

run: ## Inicia el servidor de la IA
	@echo "Iniciando servidor en http://localhost:8000..."
	@$(PYTHON) $(SERVER_FILE)

clean: ## Limpia archivos temporales de Python
	@echo "Limpiando..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf *.pyc

kill: ## Detiene el servidor que esté escuchando en el puerto 8000
	@fuser -k 8000/tcp || echo "No hay servidor corriendo en el puerto 8000"