# 🚀 Guía de Inicio Rápido

Esta guía te ayudará a empezar a usar el Sistema de Estudio de Contabilidad en minutos.

## ⚡ Pasos Rápidos

### 1. Preparar el Entorno

```bash
# Clonar repositorio (si no lo has hecho)
git clone https://github.com/diegobravomo/Contabilidad-Financiera.git
cd Contabilidad-Financiera

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar API Key

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tu editor favorito
# Reemplazar "tu-clave-de-api-aqui" con tu clave real de OpenAI
nano .env  # o vim .env, o code .env, etc.
```

Tu archivo `.env` debe verse así:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

### 3. Añadir Documentos

```bash
# Crear carpeta data si no existe
mkdir -p data

# Copiar tus PDFs a la carpeta data
cp ~/Documents/NIIF/*.pdf data/
# O simplemente arrastrar archivos a la carpeta data/
```

### 4. Validar Instalación

```bash
# Ejecutar script de validación
python validate.py
```

Si todo está bien, verás:
```
✓ TODAS LAS VERIFICACIONES PASARON
```

### 5. Procesar Documentos

```bash
# Primera vez: procesar todos los documentos
python ingest.py

# Esto tomará unos minutos...
# Verás progreso como:
# [1/4] Procesando documentos...
# [2/4] Preparando almacén vectorial...
# [3/4] Vectorizando documentos...
# [4/4] Verificando ingesta...
```

### 6. ¡Iniciar la Aplicación!

```bash
# Ejecutar Streamlit
streamlit run app.py
```

La aplicación se abrirá en tu navegador: `http://localhost:8501`

## 🎯 Primer Uso

### Chat con Documentos
1. Ve a la pestaña **"💬 Chat"**
2. Escribe: "¿Qué es la depreciación?"
3. ¡Recibe una respuesta basada en tus documentos!

### Generar Resumen
1. Ve a la pestaña **"📝 Resúmenes"**
2. Buscar en documentos → Tema: "Estados Financieros"
3. Click en "Generar Resumen"
4. ¡Lee el resumen estructurado!

### Crear Quiz
1. Ve a la pestaña **"🎯 Quizzes"**
2. Tema: "Activos"
3. Número de preguntas: 5
4. Click en "Generar Quiz"
5. ¡Responde y ve tu calificación!

## ⚠️ Solución de Problemas Comunes

### "OPENAI_API_KEY no está configurada"
→ Asegúrate de crear el archivo `.env` con tu clave

### "No se ha encontrado la base de datos"
→ Ejecuta `python ingest.py` primero

### "Error al cargar PDF"
→ Verifica que los PDFs tengan texto extraíble (no solo imágenes)

### "ModuleNotFoundError"
→ Instala dependencias: `pip install -r requirements.txt`

### "streamlit: command not found"
→ Activa el entorno virtual: `source venv/bin/activate`

## 📚 Documentos de Ejemplo

Si no tienes documentos, puedes buscar PDFs de:
- **NIIF/NIC**: Sitio oficial de IFRS Foundation
- **Material educativo**: Libros de contabilidad (respetando copyright)
- **Apuntes propios**: Tus propias notas de clase

## 🔄 Añadir Más Documentos

```bash
# Copiar nuevos PDFs a data/
cp nuevos_documentos/*.pdf data/

# Re-ejecutar ingesta (añadirá los nuevos)
python ingest.py

# O forzar recreación completa
python ingest.py --force-recreate
```

## 💡 Consejos Pro

1. **Organiza tus PDFs**: Crea subcarpetas en `data/` por tema
2. **Nombres descriptivos**: Nombra tus PDFs claramente
3. **Calidad importa**: Usa PDFs con texto extraíble
4. **Experimenta**: Prueba diferentes preguntas y temas
5. **Historial**: Usa el chat para hacer preguntas de seguimiento

## 📖 Más Información

- **README completo**: Ver `README.md`
- **Documentación de módulos**: Ver comentarios en código fuente
- **Configuración avanzada**: Ver `config/settings.py`

## 🆘 Ayuda

Si tienes problemas:
1. Ejecuta `python validate.py` para diagnóstico
2. Revisa los logs en la terminal
3. Consulta el README completo
4. Abre un issue en GitHub

---

**¡Listo! Ahora estás preparado para estudiar contabilidad con IA 🎓**
