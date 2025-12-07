# 📊 Sistema de Estudio de Contabilidad Financiera

Sistema inteligente para estudiar Contabilidad Financiera utilizando Inteligencia Artificial, RAG (Retrieval-Augmented Generation) y procesamiento de documentos PDF/NIIF.

## 🎯 Características

- **💬 Chat con Documentos**: Realiza preguntas sobre contabilidad y obtén respuestas fundamentadas en tus documentos (NIIF, libros, apuntes)
- **📝 Generación de Resúmenes**: Crea resúmenes automáticos de conceptos contables complejos
- **🎯 Quizzes Interactivos**: Genera cuestionarios automáticos para practicar y evaluar conocimientos
- **🔍 Búsqueda Semántica**: Encuentra información relevante incluso sin coincidencias exactas de palabras
- **📚 Base de Conocimiento**: Almacena y consulta múltiples documentos contables de manera eficiente

## 🏗️ Arquitectura

### Stack Tecnológico

- **LangChain**: Framework para aplicaciones con LLMs y RAG
- **ChromaDB**: Base de datos vectorial para almacenamiento de embeddings
- **OpenAI**: Modelos de lenguaje (GPT-3.5-turbo) y embeddings
- **Streamlit**: Interfaz de usuario interactiva
- **Pandas**: Análisis de datos
- **Python 3.8+**: Lenguaje de programación

### Estructura del Proyecto

```
Contabilidad-Financiera/
├── app.py                      # Aplicación principal Streamlit
├── ingest.py                   # Script de ingesta de documentos
├── requirements.txt            # Dependencias del proyecto
├── .env.example               # Ejemplo de configuración
├── .gitignore                 # Archivos a ignorar por git
├── README.md                  # Este archivo
│
├── config/                    # Configuración del sistema
│   ├── __init__.py
│   └── settings.py           # Configuraciones centralizadas
│
├── src/                      # Código fuente modular
│   ├── __init__.py
│   ├── document_processor.py    # Procesamiento de PDFs
│   ├── vector_store.py          # Gestión de ChromaDB
│   ├── chat_engine.py           # Motor de chat con RAG
│   ├── summary_generator.py     # Generación de resúmenes
│   └── quiz_generator.py        # Generación de quizzes
│
├── data/                     # Documentos PDF (NIIF, libros, apuntes)
│   └── [tus PDFs aquí]
│
├── database/                 # Base de datos ChromaDB (generada)
│   └── chroma/
│
└── tests/                    # Tests unitarios
    └── [tests aquí]
```

## 🚀 Instalación

### Prerequisitos

- Python 3.8 o superior
- Cuenta de OpenAI con API Key
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/diegobravomo/Contabilidad-Financiera.git
cd Contabilidad-Financiera
```

2. **Crear entorno virtual**
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y añadir tu API key de OpenAI
# OPENAI_API_KEY=tu-clave-aqui
```

5. **Preparar documentos**
```bash
# Colocar tus PDFs en la carpeta data/
mkdir -p data
# Copia tus documentos PDF de contabilidad a la carpeta data/
```

## 📖 Uso

### 1. Procesar Documentos (Ingesta)

Primero, debes procesar tus documentos PDF para crear la base de datos vectorial:

```bash
# Procesar todos los PDFs en la carpeta data/
python ingest.py

# O procesar un archivo específico
python ingest.py data/niif_9.pdf

# Forzar recreación de la base de datos
python ingest.py --force-recreate
```

Este proceso:
- Lee los PDFs
- Los divide en fragmentos manejables
- Genera embeddings (vectorizaciones)
- Los almacena en ChromaDB

**Nota**: La primera vez puede tardar varios minutos dependiendo de la cantidad de documentos.

### 2. Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

### 3. Usar las Funcionalidades

#### 💬 Chat con Documentos

1. Ve a la pestaña "Chat"
2. Escribe tu pregunta sobre contabilidad
3. El sistema buscará información relevante en tus documentos
4. Recibirás una respuesta con referencias a las fuentes

**Ejemplos de preguntas:**
- "¿Qué es la depreciación según NIIF?"
- "Explica el concepto de valor razonable"
- "¿Cómo se registra una provisión?"
- "Diferencias entre método directo e indirecto"

#### 📝 Generador de Resúmenes

1. Ve a la pestaña "Resúmenes"
2. Elige entre:
   - **Buscar en documentos**: Busca un tema y genera resumen
   - **Texto personalizado**: Pega texto y genera resumen
3. Haz clic en "Generar Resumen"
4. Obtén un resumen estructurado con puntos clave

#### 🎯 Generador de Quizzes

1. Ve a la pestaña "Quizzes"
2. Ingresa un tema contable
3. Selecciona número de preguntas y dificultad
4. Haz clic en "Generar Quiz"
5. Responde las preguntas
6. Envía y recibe calificación con explicaciones

## 🧩 Módulos Principales

### DocumentProcessor
Procesa documentos PDF y los divide en fragmentos para vectorización.

```python
from src import DocumentProcessor

processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
documents = processor.process_documents("data/")
```

### VectorStore
Gestiona el almacenamiento y búsqueda de vectores en ChromaDB.

```python
from src import VectorStore

vector_store = VectorStore(
    persist_directory="database/chroma",
    collection_name="contabilidad_financiera"
)
vector_store.create_vector_store(documents)
```

### ChatEngine
Motor de chat conversacional con RAG.

```python
from src import ChatEngine

chat_engine = ChatEngine(retriever=retriever)
response = chat_engine.chat("¿Qué es la depreciación?")
print(response["answer"])
```

### SummaryGenerator
Genera resúmenes de textos contables.

```python
from src import SummaryGenerator

generator = SummaryGenerator()
summary = generator.generate_summary(text)
print(summary)
```

### QuizGenerator
Genera cuestionarios automáticos.

```python
from src import QuizGenerator

quiz_gen = QuizGenerator()
quiz = quiz_gen.generate_quiz(text, num_questions=5)
for q in quiz:
    print(q.format_for_display())
```

## 🎓 Conceptos Educativos

### Programación Orientada a Objetos (POO)

El proyecto utiliza POO con clases bien definidas:
- **Encapsulación**: Cada clase gestiona su propia lógica
- **Abstracción**: Interfaces claras y métodos bien documentados
- **Modularidad**: Componentes independientes y reutilizables

### RAG (Retrieval-Augmented Generation)

El sistema implementa RAG para combinar:
1. **Retrieval**: Búsqueda de información relevante en documentos
2. **Augmentation**: Enriquecimiento del contexto del LLM
3. **Generation**: Generación de respuestas fundamentadas

### Principios de Código Limpio

- Nombres descriptivos y significativos
- Funciones pequeñas con responsabilidad única
- Comentarios educativos sobre lógica contable
- Manejo apropiado de errores
- Logging para debugging

## 🔧 Configuración Avanzada

### Modificar Parámetros

Edita `config/settings.py` para ajustar:

```python
# Tamaño de fragmentos de texto
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Modelo de chat
CHAT_MODEL = "gpt-3.5-turbo"  # o "gpt-4"
CHAT_TEMPERATURE = 0.7

# Modelo de embeddings
EMBEDDING_MODEL = "text-embedding-ada-002"
```

### Personalizar Prompts

Los prompts del sistema se encuentran en `config/settings.py`:
- `CHAT_SYSTEM_PROMPT`: Comportamiento del asistente de chat
- `SUMMARY_PROMPT`: Estructura de resúmenes
- `QUIZ_PROMPT`: Formato de quizzes

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
pytest tests/

# Con cobertura
pytest --cov=src tests/
```

## 📊 Ejemplo de Flujo de Trabajo

1. **Preparación**:
   ```bash
   # Añadir PDFs a data/
   cp ~/Descargas/NIIF/*.pdf data/
   ```

2. **Ingesta**:
   ```bash
   python ingest.py
   ```

3. **Estudio**:
   ```bash
   streamlit run app.py
   ```

4. **Workflow de estudio**:
   - Leer material con el generador de resúmenes
   - Consultar dudas en el chat
   - Practicar con quizzes
   - Repetir para diferentes temas

## 🤝 Contribuir

Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

**Diego Bravo**
- GitHub: [@diegobravomo](https://github.com/diegobravomo)

## 🙏 Agradecimientos

- OpenAI por los modelos de lenguaje
- LangChain por el framework
- Streamlit por la interfaz de usuario
- La comunidad de código abierto

## 📧 Soporte

Si tienes preguntas o problemas:
1. Revisa la documentación
2. Busca en los issues existentes
3. Abre un nuevo issue si es necesario

## 🔮 Roadmap

- [ ] Soporte para más formatos de documentos (Word, Excel)
- [ ] Análisis de estados financieros
- [ ] Generación de ejercicios prácticos
- [ ] Sistema de flashcards
- [ ] Exportación de resúmenes a PDF
- [ ] Modo offline con modelos locales
- [ ] Soporte multiidioma

---

**⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub!**
