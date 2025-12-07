"""
Configuración del Sistema de Estudio de Contabilidad
Este archivo centraliza todas las configuraciones del sistema.
"""
import os
from pathlib import Path

# Directorios del Proyecto
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"
SRC_DIR = BASE_DIR / "src"

# Configuración de ChromaDB
CHROMA_COLLECTION_NAME = "contabilidad_financiera"
CHROMA_PERSIST_DIRECTORY = str(DATABASE_DIR / "chroma")

# Configuración del Modelo de Embeddings
EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI embedding model

# Configuración del Modelo de Chat
CHAT_MODEL = "gpt-3.5-turbo"
CHAT_TEMPERATURE = 0.7

# Configuración de Procesamiento de Documentos
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Configuración de la Interfaz Streamlit
APP_TITLE = "Sistema de Estudio de Contabilidad Financiera"
APP_ICON = "📊"

# Prompt Templates
CHAT_SYSTEM_PROMPT = """Eres un profesor experto en Contabilidad Financiera y Normas Internacionales de Información Financiera (NIIF).
Tu objetivo es ayudar a los estudiantes a comprender conceptos contables complejos de manera clara y educativa.
Responde basándote en la información de los documentos proporcionados y proporciona ejemplos prácticos cuando sea apropiado.
Si no encuentras información relevante en los documentos, indícalo claramente."""

SUMMARY_PROMPT = """Resume el siguiente texto sobre contabilidad financiera de manera clara y estructurada.
Enfócate en los conceptos clave, definiciones importantes y principios contables relevantes.
Organiza el resumen en puntos principales y subpuntos cuando sea necesario.

Texto:
{text}

Resumen:"""

QUIZ_PROMPT = """Basándote en el siguiente contenido sobre contabilidad financiera, genera {num_questions} preguntas de opción múltiple.
Cada pregunta debe tener 4 opciones (A, B, C, D) y una respuesta correcta claramente identificada.
Las preguntas deben evaluar la comprensión de conceptos contables importantes.

Formato de salida:
Pregunta 1: [texto de la pregunta]
A) [opción A]
B) [opción B]
C) [opción C]
D) [opción D]
Respuesta correcta: [letra]
Explicación: [breve explicación de por qué es correcta]

Contenido:
{text}

Preguntas:"""

# Configuración de OpenAI (se carga desde variables de entorno)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
