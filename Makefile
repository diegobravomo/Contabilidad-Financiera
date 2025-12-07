# Makefile para Sistema de Estudio de Contabilidad
# Facilita la ejecución de comandos comunes

.PHONY: help install validate ingest run clean test

# Comando por defecto
help:
	@echo "Sistema de Estudio de Contabilidad Financiera"
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  make install     - Instalar dependencias"
	@echo "  make validate    - Validar instalación"
	@echo "  make ingest      - Procesar documentos"
	@echo "  make run         - Ejecutar aplicación Streamlit"
	@echo "  make clean       - Limpiar archivos temporales"
	@echo "  make test        - Ejecutar tests (futuro)"
	@echo "  make setup       - Setup completo (install + validate)"

# Instalar dependencias
install:
	pip install -r requirements.txt

# Validar instalación
validate:
	python validate.py

# Procesar documentos
ingest:
	python ingest.py

# Procesar documentos (forzar recreación)
ingest-force:
	python ingest.py --force-recreate

# Ejecutar aplicación
run:
	streamlit run app.py

# Setup completo
setup: install validate
	@echo "Setup completado. Próximos pasos:"
	@echo "1. Configurar .env con OPENAI_API_KEY"
	@echo "2. Añadir PDFs a data/"
	@echo "3. Ejecutar: make ingest"
	@echo "4. Ejecutar: make run"

# Limpiar archivos temporales
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# Limpiar completamente (incluye base de datos)
clean-all: clean
	rm -rf database/

# Ejecutar tests (cuando estén implementados)
test:
	pytest tests/ -v

# Ejecutar tests con cobertura
test-cov:
	pytest --cov=src tests/

# Formatear código (requiere black)
format:
	black src/ tests/ *.py

# Lint código (requiere flake8)
lint:
	flake8 src/ tests/ *.py --max-line-length=100
