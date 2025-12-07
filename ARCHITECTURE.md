# 🏗️ Arquitectura del Sistema

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                    USUARIO (Estudiante)                          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              INTERFAZ STREAMLIT (app.py)                         │
│  ┌──────────┐   ┌──────────┐   ┌──────────────┐                │
│  │   Chat   │   │ Resúmenes│   │   Quizzes    │                │
│  └──────────┘   └──────────┘   └──────────────┘                │
└─────────┬──────────┬────────────────┬───────────────────────────┘
          │          │                │
          ▼          ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CAPA DE SERVICIOS (src/)                       │
│  ┌──────────────┐  ┌─────────────────┐  ┌──────────────┐       │
│  │ ChatEngine   │  │ SummaryGenerator│  │QuizGenerator │       │
│  │   (RAG)      │  │   (LLM)         │  │   (LLM)      │       │
│  └──────┬───────┘  └────────┬────────┘  └──────┬───────┘       │
│         │                   │                   │                │
│         └───────────────────┴───────────────────┘                │
│                             │                                    │
│                   ┌─────────▼─────────┐                         │
│                   │   VectorStore     │                         │
│                   │   (ChromaDB)      │                         │
│                   └─────────┬─────────┘                         │
└─────────────────────────────┼─────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│               PROCESAMIENTO (ingest.py)                          │
│  ┌──────────────────────────────────────────────┐               │
│  │         DocumentProcessor                     │               │
│  │  ┌───────────┐  ┌──────────┐  ┌──────────┐  │               │
│  │  │ Load PDF  │→ │  Split   │→ │ Vectorize│  │               │
│  │  └───────────┘  └──────────┘  └──────────┘  │               │
│  └──────────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA DE DATOS                                 │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │ data/        │         │ database/    │                     │
│  │ (PDFs)       │         │ (ChromaDB)   │                     │
│  └──────────────┘         └──────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SERVICIOS EXTERNOS                              │
│                    OpenAI API                                    │
│         ┌─────────────┐    ┌─────────────┐                     │
│         │ Embeddings  │    │     LLM     │                     │
│         │(ada-002)    │    │(GPT-3.5)    │                     │
│         └─────────────┘    └─────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

## Flujo de Datos

### 1. Ingesta de Documentos
```
PDFs → DocumentProcessor → Chunks → OpenAI Embeddings → ChromaDB
```

### 2. Consulta de Chat
```
Pregunta Usuario → VectorStore.search() → Documentos Relevantes
                                                ↓
                         ChatEngine → OpenAI LLM → Respuesta
```

### 3. Generación de Resumen
```
Tema → VectorStore.search() → Documentos → SummaryGenerator → Resumen
```

### 4. Generación de Quiz
```
Tema → VectorStore.search() → Documentos → QuizGenerator → Preguntas
```

## Componentes Principales

### app.py (Streamlit UI)
- **Responsabilidad**: Interfaz de usuario
- **Tecnología**: Streamlit
- **Componentes**:
  - Chat tab: Interfaz conversacional
  - Summary tab: Generación de resúmenes
  - Quiz tab: Creación y resolución de quizzes

### ingest.py (Procesamiento)
- **Responsabilidad**: Ingesta de documentos
- **Proceso**:
  1. Carga PDFs
  2. Divide en chunks
  3. Genera embeddings
  4. Persiste en ChromaDB

### src/document_processor.py
- **Clase**: `DocumentProcessor`
- **Funciones**:
  - `load_pdf()`: Carga PDF individual
  - `load_directory()`: Carga múltiples PDFs
  - `split_documents()`: Divide en chunks
  - `process_documents()`: Pipeline completo

### src/vector_store.py
- **Clase**: `VectorStore`
- **Funciones**:
  - `create_vector_store()`: Crea BD vectorial
  - `load_vector_store()`: Carga BD existente
  - `similarity_search()`: Búsqueda semántica
  - `as_retriever()`: Convierte a retriever

### src/chat_engine.py
- **Clase**: `ChatEngine`
- **Patrón**: RAG (Retrieval-Augmented Generation)
- **Funciones**:
  - `chat()`: Procesa pregunta con contexto
  - `format_sources()`: Formatea referencias
  - `clear_conversation_history()`: Limpia historial

### src/summary_generator.py
- **Clase**: `SummaryGenerator`
- **Estrategias**:
  - Textos cortos: Directo
  - Textos largos: Refinamiento
- **Funciones**:
  - `generate_summary()`: Resumen general
  - `generate_key_points()`: Puntos clave
  - `generate_concept_map()`: Mapa conceptual

### src/quiz_generator.py
- **Clases**: `QuizGenerator`, `QuizQuestion`
- **Funciones**:
  - `generate_quiz()`: Genera cuestionario
  - `check_answer()`: Verifica respuesta
  - `score_quiz()`: Califica quiz completo

## Patrones de Diseño

### 1. Repository Pattern
`VectorStore` abstrae operaciones de persistencia

### 2. Strategy Pattern
`DocumentProcessor` permite diferentes métodos de carga

### 3. Facade Pattern
Clases de alto nivel simplifican complejidad interna

### 4. Builder Pattern
Construcción incremental de documentos y preguntas

## Configuración (config/settings.py)

Centraliza todas las configuraciones:
- Rutas de directorios
- Parámetros de modelos
- Configuración de ChromaDB
- Prompts del sistema

## Dependencias Clave

```
LangChain ─┬─→ Orquestación de LLMs
           ├─→ RAG pipeline
           └─→ Document loaders

ChromaDB ──→ Base de datos vectorial

OpenAI ────┬─→ Embeddings (ada-002)
           └─→ LLM (GPT-3.5-turbo)

Streamlit ─→ Interfaz de usuario

Pandas ────→ Análisis de datos (futuro)
```

## Escalabilidad

### Actual
- Procesamiento local
- ChromaDB local
- API calls a OpenAI

### Futuro (Posibles mejoras)
- BD vectorial distribuida (Pinecone, Weaviate)
- Cache de embeddings
- Paralelización de procesamiento
- API REST para backend
- Despliegue en cloud

## Seguridad

### Implementado
- API keys en variables de entorno
- .gitignore para secretos
- Logging de errores (sin datos sensibles)

### Recomendado
- Validación de entrada
- Rate limiting
- Autenticación de usuarios
- Encriptación de datos sensibles

## Testing

### Estructura (futuro)
```
tests/
├── test_document_processor.py
├── test_vector_store.py
├── test_chat_engine.py
├── test_summary_generator.py
└── test_quiz_generator.py
```

### Tipos
- Unit tests: Funciones individuales
- Integration tests: Flujos completos
- E2E tests: Streamlit UI

## Monitoreo y Logs

### Niveles de Log
- INFO: Operaciones normales
- WARNING: Situaciones inusuales
- ERROR: Errores recuperables
- CRITICAL: Errores fatales

### Métricas Importantes
- Tiempo de ingesta
- Latencia de respuestas
- Uso de tokens OpenAI
- Tamaño de BD vectorial

---

**Nota**: Esta arquitectura prioriza claridad educativa y mantenibilidad sobre optimización prematura.
