"""
Aplicación Streamlit - Sistema de Estudio de Contabilidad Financiera

Esta aplicación proporciona una interfaz interactiva para estudiar
contabilidad financiera utilizando IA y documentos procesados.

Funcionalidades:
1. Chat con documentos contables (RAG)
2. Generación de resúmenes automáticos
3. Generación de quizzes automáticos
4. Análisis de conceptos clave

Conceptos Contables:
- La aplicación funciona como un asistente educativo integral,
  similar a cómo un sistema ERP integra diferentes módulos contables.
- Proporciona trazabilidad y referencias, como las notas a los
  estados financieros.
"""

import sys
from pathlib import Path
import os
import logging

import streamlit as st
from dotenv import load_dotenv

# Añadir directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from src import (
    VectorStore,
    ChatEngine,
    SummaryGenerator,
    QuizGenerator
)
from config.settings import (
    CHROMA_PERSIST_DIRECTORY,
    CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL,
    CHAT_MODEL,
    CHAT_TEMPERATURE,
    APP_TITLE,
    APP_ICON
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()


def init_session_state():
    """
    Inicializa el estado de la sesión de Streamlit.
    
    Concepto Contable:
        El estado de sesión es como mantener un libro mayor de trabajo
        donde se registran las interacciones durante una sesión de estudio.
    """
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
        st.session_state.vector_store = None
        st.session_state.chat_engine = None
        st.session_state.summary_generator = None
        st.session_state.quiz_generator = None
        st.session_state.chat_history = []
        st.session_state.current_quiz = []
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False


def check_environment():
    """
    Verifica que el entorno esté configurado correctamente.
    
    Returns:
        Tuple (bool, str): (configurado correctamente, mensaje de error si hay)
    """
    # Verificar API key
    if not os.getenv("OPENAI_API_KEY"):
        return False, "⚠️ OPENAI_API_KEY no está configurada. Por favor, crea un archivo .env con tu clave de API."
    
    # Verificar que existe el almacén vectorial
    if not Path(CHROMA_PERSIST_DIRECTORY).exists():
        return False, "⚠️ No se ha encontrado la base de datos de documentos. Por favor, ejecuta primero `python ingest.py` para procesar tus documentos."
    
    return True, ""


def initialize_components():
    """
    Inicializa los componentes principales de la aplicación.
    
    Concepto Contable:
        Similar a la apertura de libros contables al inicio de un período,
        inicializamos todos los sistemas necesarios para operar.
    """
    try:
        with st.spinner("Inicializando sistema..."):
            # Inicializar Vector Store
            vector_store_manager = VectorStore(
                persist_directory=CHROMA_PERSIST_DIRECTORY,
                collection_name=CHROMA_COLLECTION_NAME,
                embedding_model=EMBEDDING_MODEL
            )
            st.session_state.vector_store = vector_store_manager.load_vector_store()
            
            # Crear retriever
            retriever = vector_store_manager.as_retriever(search_kwargs={"k": 4})
            
            # Inicializar Chat Engine
            st.session_state.chat_engine = ChatEngine(
                retriever=retriever,
                model_name=CHAT_MODEL,
                temperature=CHAT_TEMPERATURE
            )
            
            # Inicializar generadores
            st.session_state.summary_generator = SummaryGenerator()
            st.session_state.quiz_generator = QuizGenerator()
            
            st.session_state.initialized = True
            logger.info("Componentes inicializados exitosamente")
            
    except Exception as e:
        st.error(f"Error al inicializar componentes: {str(e)}")
        logger.error(f"Error en initialize_components: {str(e)}", exc_info=True)
        st.session_state.initialized = False


def render_sidebar():
    """
    Renderiza la barra lateral con información y controles.
    """
    with st.sidebar:
        st.title("📚 Sistema de Estudio")
        st.markdown("---")
        
        st.markdown("""
        ### Sobre esta aplicación
        
        Sistema inteligente para estudiar **Contabilidad Financiera** 
        utilizando IA y procesamiento de documentos.
        
        **Funcionalidades:**
        - 💬 Chat con documentos
        - 📝 Resúmenes automáticos
        - 🎯 Quizzes interactivos
        """)
        
        st.markdown("---")
        
        # Estadísticas
        if st.session_state.initialized and st.session_state.vector_store:
            st.markdown("### 📊 Estadísticas")
            try:
                doc_count = st.session_state.vector_store._collection.count()
                st.metric("Documentos en BD", doc_count)
            except:
                pass
        
        st.markdown("---")
        
        # Limpiar historial
        if st.button("🗑️ Limpiar Historial de Chat"):
            if st.session_state.chat_engine:
                st.session_state.chat_engine.clear_conversation_history()
                st.session_state.chat_history = []
                st.success("Historial limpiado")
                st.rerun()
        
        st.markdown("---")
        st.markdown("""
        ### 💡 Consejos
        - Haz preguntas específicas sobre conceptos contables
        - Usa el generador de resúmenes para estudiar temas largos
        - Practica con quizzes para reforzar conocimientos
        """)


def chat_tab():
    """
    Pestaña de chat con documentos.
    
    Concepto Contable:
        El chat funciona como consultar a un contador experto que tiene
        acceso a toda la normativa y documentación relevante.
    """
    st.header("💬 Chat con Documentos Contables")
    st.markdown("""
    Haz preguntas sobre contabilidad financiera y recibirás respuestas 
    basadas en tus documentos cargados.
    """)
    
    # Mostrar historial de chat
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Mostrar fuentes si existen
                if "sources" in message and message["sources"]:
                    with st.expander("📚 Ver fuentes"):
                        st.markdown(message["sources"])
    
    # Input de usuario
    if prompt := st.chat_input("Escribe tu pregunta sobre contabilidad..."):
        # Añadir mensaje del usuario al historial
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generar respuesta
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = st.session_state.chat_engine.chat(prompt)
                
                # Mostrar respuesta
                st.markdown(response["answer"])
                
                # Formatear y mostrar fuentes
                if response["has_sources"]:
                    sources_formatted = st.session_state.chat_engine.format_sources(
                        response["source_documents"]
                    )
                    with st.expander("📚 Ver fuentes"):
                        st.markdown(sources_formatted)
                    
                    # Añadir al historial con fuentes
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response["answer"],
                        "sources": sources_formatted
                    })
                else:
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response["answer"]
                    })


def summary_tab():
    """
    Pestaña de generación de resúmenes.
    
    Concepto Contable:
        Los resúmenes son como las notas explicativas: condensan
        información compleja en formatos más digeribles.
    """
    st.header("📝 Generador de Resúmenes")
    st.markdown("""
    Genera resúmenes automáticos de conceptos contables o textos extensos.
    """)
    
    # Dos opciones: desde búsqueda o desde texto
    option = st.radio(
        "Selecciona la fuente:",
        ["Buscar en documentos", "Texto personalizado"]
    )
    
    if option == "Buscar en documentos":
        query = st.text_input(
            "¿Qué tema contable quieres resumir?",
            placeholder="Ej: Depreciación de activos fijos"
        )
        
        num_docs = st.slider("Número de documentos a incluir", 1, 10, 3)
        
        if st.button("Generar Resumen", type="primary"):
            if query:
                with st.spinner("Buscando información y generando resumen..."):
                    try:
                        # Buscar documentos relevantes
                        retriever = st.session_state.vector_store.as_retriever(
                            search_kwargs={"k": num_docs}
                        )
                        docs = retriever.get_relevant_documents(query)
                        
                        if docs:
                            # Generar resumen
                            summary = st.session_state.summary_generator.summarize_documents(
                                docs,
                                combine=True
                            )
                            
                            st.success("Resumen generado!")
                            st.markdown("### 📄 Resumen")
                            st.markdown(summary)
                            
                            # Mostrar fuentes
                            with st.expander("📚 Documentos utilizados"):
                                for i, doc in enumerate(docs, 1):
                                    source = doc.metadata.get('source', 'Desconocido')
                                    st.markdown(f"**{i}.** {Path(source).name}")
                        else:
                            st.warning("No se encontraron documentos relevantes.")
                    except Exception as e:
                        st.error(f"Error al generar resumen: {str(e)}")
            else:
                st.warning("Por favor, ingresa un tema a resumir.")
    
    else:  # Texto personalizado
        text = st.text_area(
            "Pega aquí el texto que deseas resumir:",
            height=200,
            placeholder="Ingresa el texto sobre contabilidad..."
        )
        
        if st.button("Generar Resumen", type="primary"):
            if text:
                with st.spinner("Generando resumen..."):
                    try:
                        summary = st.session_state.summary_generator.generate_summary(text)
                        
                        st.success("Resumen generado!")
                        st.markdown("### 📄 Resumen")
                        st.markdown(summary)
                        
                        # Generar puntos clave
                        st.markdown("### 🎯 Puntos Clave")
                        key_points = st.session_state.summary_generator.generate_key_points(text, 5)
                        for i, point in enumerate(key_points, 1):
                            st.markdown(f"{i}. {point}")
                    except Exception as e:
                        st.error(f"Error al generar resumen: {str(e)}")
            else:
                st.warning("Por favor, ingresa texto para resumir.")


def quiz_tab():
    """
    Pestaña de generación y resolución de quizzes.
    
    Concepto Contable:
        Los quizzes son herramientas de evaluación, similares a controles
        internos que verifican el conocimiento y comprensión.
    """
    st.header("🎯 Generador de Quizzes")
    st.markdown("""
    Genera quizzes automáticos para practicar conceptos contables.
    """)
    
    # Si no hay quiz activo, mostrar opciones de generación
    if not st.session_state.current_quiz:
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input(
                "Tema contable:",
                placeholder="Ej: Estados Financieros"
            )
        
        with col2:
            num_questions = st.number_input(
                "Número de preguntas:",
                min_value=1,
                max_value=10,
                value=5
            )
        
        difficulty = st.select_slider(
            "Nivel de dificultad:",
            options=["easy", "medium", "hard"],
            value="medium"
        )
        
        if st.button("Generar Quiz", type="primary"):
            if topic:
                with st.spinner("Generando quiz..."):
                    try:
                        # Buscar información sobre el tema
                        retriever = st.session_state.vector_store.as_retriever(
                            search_kwargs={"k": 3}
                        )
                        docs = retriever.get_relevant_documents(topic)
                        
                        if docs:
                            # Generar quiz
                            quiz = st.session_state.quiz_generator.generate_quiz_from_documents(
                                docs,
                                num_questions=num_questions,
                                difficulty=difficulty
                            )
                            
                            if quiz:
                                st.session_state.current_quiz = quiz
                                st.session_state.quiz_answers = {}
                                st.session_state.quiz_submitted = False
                                st.success(f"Quiz generado con {len(quiz)} preguntas!")
                                st.rerun()
                            else:
                                st.error("No se pudieron generar preguntas. Intenta con otro tema.")
                        else:
                            st.warning("No se encontró información sobre ese tema.")
                    except Exception as e:
                        st.error(f"Error al generar quiz: {str(e)}")
            else:
                st.warning("Por favor, ingresa un tema.")
    
    else:
        # Mostrar quiz activo
        st.markdown(f"### 📝 Quiz: {len(st.session_state.current_quiz)} preguntas")
        
        if not st.session_state.quiz_submitted:
            # Mostrar preguntas
            for i, question in enumerate(st.session_state.current_quiz):
                st.markdown(f"**Pregunta {i+1}:**")
                st.markdown(question.question)
                
                # Opciones de respuesta
                answer = st.radio(
                    f"Selecciona tu respuesta:",
                    options=["A", "B", "C", "D"],
                    format_func=lambda x: f"{x}) {question.options[ord(x) - 65]}",
                    key=f"q_{i}"
                )
                
                st.session_state.quiz_answers[i] = answer
                st.markdown("---")
            
            # Botones
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Enviar Respuestas", type="primary"):
                    st.session_state.quiz_submitted = True
                    st.rerun()
            with col2:
                if st.button("Cancelar Quiz"):
                    st.session_state.current_quiz = []
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.rerun()
        
        else:
            # Mostrar resultados
            user_answers = [
                st.session_state.quiz_answers.get(i, "")
                for i in range(len(st.session_state.current_quiz))
            ]
            
            results = st.session_state.quiz_generator.score_quiz(
                st.session_state.current_quiz,
                user_answers
            )
            
            # Mostrar puntuación
            st.markdown("### 🎓 Resultados")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Correctas", results["correct_answers"])
            with col2:
                st.metric("Incorrectas", results["incorrect_answers"])
            with col3:
                st.metric("Porcentaje", f"{results['percentage']}%")
            
            st.markdown(f"### Calificación: {results['grade']}")
            
            # Mostrar detalle de cada pregunta
            st.markdown("### 📊 Detalle de Respuestas")
            for result in results["results"]:
                q_num = result["question_number"]
                
                if result["is_correct"]:
                    st.success(f"✅ Pregunta {q_num}")
                else:
                    st.error(f"❌ Pregunta {q_num}")
                
                st.markdown(f"**{result['question_text']}**")
                st.markdown(f"Tu respuesta: {result['user_answer']}")
                st.markdown(f"Respuesta correcta: {result['correct_answer']}")
                st.info(result["explanation"])
                st.markdown("---")
            
            # Botón para nuevo quiz
            if st.button("Generar Nuevo Quiz", type="primary"):
                st.session_state.current_quiz = []
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()


def main():
    """
    Función principal de la aplicación Streamlit.
    """
    # Configuración de la página
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Título principal
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.markdown("""
    Bienvenido al sistema inteligente para estudiar contabilidad financiera.
    Utiliza IA para chatear con documentos, generar resúmenes y practicar con quizzes.
    """)
    
    # Inicializar estado de sesión
    init_session_state()
    
    # Verificar entorno
    env_ok, error_msg = check_environment()
    if not env_ok:
        st.error(error_msg)
        st.info("Instrucciones:")
        st.markdown("""
        1. Crea un archivo `.env` con tu clave de API de OpenAI:
           ```
           OPENAI_API_KEY=tu-clave-aqui
           ```
        2. Coloca tus documentos PDF en la carpeta `data/`
        3. Ejecuta `python ingest.py` para procesar los documentos
        4. Recarga esta aplicación
        """)
        return
    
    # Inicializar componentes si es necesario
    if not st.session_state.initialized:
        initialize_components()
    
    # Verificar que la inicialización fue exitosa
    if not st.session_state.initialized:
        st.error("No se pudieron inicializar los componentes. Verifica los logs.")
        return
    
    # Renderizar sidebar
    render_sidebar()
    
    # Pestañas principales
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📝 Resúmenes", "🎯 Quizzes"])
    
    with tab1:
        chat_tab()
    
    with tab2:
        summary_tab()
    
    with tab3:
        quiz_tab()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <small>Sistema de Estudio de Contabilidad Financiera | Powered by LangChain, OpenAI & Streamlit</small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
