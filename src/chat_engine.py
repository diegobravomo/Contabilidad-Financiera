"""
Motor de Chat - Chat Engine

Este módulo implementa el sistema de chat conversacional con RAG
(Retrieval-Augmented Generation) para consultas sobre contabilidad financiera.

Conceptos Contables Relacionados:
- RAG es como consultar a un contador experto que tiene acceso a todas
  las normas y documentos relevantes antes de responder.
- Combina el conocimiento del modelo de lenguaje con información específica
  de documentos (similar a cómo un contador aplica tanto conocimiento general
  como normativa específica).
"""

from typing import List, Dict, Optional, Any
import logging

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import BaseRetriever

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatEngine:
    """
    Motor de chat para consultas sobre contabilidad financiera.
    
    Esta clase implementa un sistema de chat conversacional que utiliza
    RAG (Retrieval-Augmented Generation) para proporcionar respuestas
    fundamentadas en documentos contables específicos.
    
    Atributos:
        llm: Modelo de lenguaje (ChatOpenAI)
        memory: Memoria conversacional para mantener contexto
        chain: Cadena de conversación con retrieval
    """
    
    def __init__(
        self,
        retriever: BaseRetriever,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ):
        """
        Inicializa el motor de chat.
        
        Args:
            retriever: Retriever configurado del almacén vectorial
            model_name: Nombre del modelo de OpenAI a utilizar
            temperature: Temperatura del modelo (0-1, mayor = más creativo)
            system_prompt: Prompt del sistema personalizado
            
        Nota Contable:
            La temperatura controla la creatividad vs. precisión. Para
            contabilidad, usamos valores moderados (0.7) que equilibran
            explicaciones claras con precisión técnica.
        """
        self.retriever = retriever
        
        # Inicializar el modelo de lenguaje
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature
        )
        
        # Configurar memoria conversacional
        # Permite que el chat "recuerde" el contexto de la conversación
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Configurar el prompt del sistema
        if system_prompt is None:
            system_prompt = self._get_default_system_prompt()
        
        # Crear la cadena conversacional con retrieval
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True,
            verbose=False
        )
        
        logger.info(f"ChatEngine inicializado con modelo {model_name}")
    
    def _get_default_system_prompt(self) -> str:
        """
        Retorna el prompt del sistema por defecto.
        
        Returns:
            String con el prompt del sistema
            
        Concepto Contable:
            Este prompt establece el "rol profesional" del asistente,
            similar a cómo un código de ética profesional define el
            comportamiento esperado de un contador.
        """
        return """Eres un profesor experto en Contabilidad Financiera y Normas Internacionales de Información Financiera (NIIF).
Tu objetivo es ayudar a los estudiantes a comprender conceptos contables complejos de manera clara y educativa.

Directrices de respuesta:
1. Basa tus respuestas en la información de los documentos proporcionados
2. Proporciona ejemplos prácticos cuando sea apropiado
3. Explica conceptos técnicos de manera accesible
4. Si no encuentras información relevante en los documentos, indícalo claramente
5. Relaciona conceptos con principios contables fundamentales cuando sea relevante
6. Usa terminología contable correcta pero explica términos técnicos

Recuerda: La precisión es fundamental en contabilidad, pero también lo es la claridad didáctica."""
    
    def chat(self, question: str) -> Dict[str, Any]:
        """
        Procesa una pregunta y genera una respuesta basada en documentos.
        
        Args:
            question: Pregunta del usuario sobre contabilidad
            
        Returns:
            Diccionario con la respuesta, documentos fuente y metadata
            
        Ejemplo de Uso:
            >>> engine = ChatEngine(retriever)
            >>> response = engine.chat("¿Qué es la depreciación según NIIF?")
            >>> print(response['answer'])
            
        Concepto Contable:
            Similar a una consulta técnica a un experto. El sistema:
            1. Busca información relevante (consulta documentos/normas)
            2. Analiza el contexto (considera principios contables)
            3. Genera respuesta fundamentada (opinión profesional)
        """
        if not question or not question.strip():
            logger.warning("Pregunta vacía recibida")
            return {
                "answer": "Por favor, formula una pregunta sobre contabilidad.",
                "source_documents": [],
                "question": question
            }
        
        try:
            logger.info(f"Procesando pregunta: {question[:100]}...")
            
            # Ejecutar la cadena de conversación
            result = self.chain({"question": question})
            
            # Extraer información relevante
            response = {
                "answer": result.get("answer", ""),
                "source_documents": result.get("source_documents", []),
                "question": question,
                "has_sources": len(result.get("source_documents", [])) > 0
            }
            
            logger.info(f"Respuesta generada con {len(response['source_documents'])} documentos fuente")
            return response
            
        except Exception as e:
            logger.error(f"Error al procesar pregunta: {str(e)}")
            return {
                "answer": f"Lo siento, ocurrió un error al procesar tu pregunta: {str(e)}",
                "source_documents": [],
                "question": question,
                "error": str(e)
            }
    
    def chat_stream(self, question: str):
        """
        Versión en streaming del chat (para futuras implementaciones).
        
        Args:
            question: Pregunta del usuario
            
        Yields:
            Fragmentos de la respuesta a medida que se generan
            
        Nota: Actualmente retorna la respuesta completa.
        Streaming completo requeriría configuración adicional de callbacks.
        """
        response = self.chat(question)
        yield response["answer"]
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Obtiene el historial de la conversación actual.
        
        Returns:
            Lista de mensajes de la conversación
            
        Concepto Contable:
            El historial conversacional es como un libro de actas o registro
            de consultas previas, útil para mantener trazabilidad de las
            interacciones y decisiones tomadas.
        """
        try:
            if hasattr(self.memory, 'chat_memory'):
                messages = self.memory.chat_memory.messages
                history = []
                for msg in messages:
                    history.append({
                        "type": msg.type,
                        "content": msg.content
                    })
                return history
            return []
        except Exception as e:
            logger.error(f"Error al obtener historial: {str(e)}")
            return []
    
    def clear_conversation_history(self) -> None:
        """
        Limpia el historial de conversación.
        
        Concepto Contable:
            Similar a iniciar un nuevo período contable o una nueva sesión
            de consulta. La información anterior no se pierde permanentemente,
            pero el contexto se reinicia para una nueva conversación.
        """
        try:
            self.memory.clear()
            logger.info("Historial de conversación limpiado")
        except Exception as e:
            logger.error(f"Error al limpiar historial: {str(e)}")
    
    def format_sources(self, source_documents: List) -> str:
        """
        Formatea los documentos fuente para mostrar al usuario.
        
        Args:
            source_documents: Lista de documentos fuente de LangChain
            
        Returns:
            String formateado con información de las fuentes
            
        Concepto Contable:
            En contabilidad, siempre debemos citar nuestras fuentes y
            referencias normativas. Esta función proporciona la trazabilidad
            necesaria para que los usuarios verifiquen la información.
        """
        if not source_documents:
            return "No se encontraron documentos fuente específicos."
        
        formatted = "**Documentos de referencia:**\n\n"
        
        for i, doc in enumerate(source_documents, 1):
            source = doc.metadata.get('source', 'Desconocido')
            page = doc.metadata.get('page', 'N/A')
            
            # Extraer solo el nombre del archivo
            if '/' in source:
                source = source.split('/')[-1]
            
            formatted += f"{i}. **{source}** (Página {page})\n"
            
            # Mostrar un fragmento del contenido
            content_preview = doc.page_content[:200].strip()
            if len(doc.page_content) > 200:
                content_preview += "..."
            
            formatted += f"   > {content_preview}\n\n"
        
        return formatted
    
    def get_relevant_context(self, question: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Obtiene contexto relevante sin generar una respuesta completa.
        
        Args:
            question: Pregunta o tema de interés
            k: Número de documentos a recuperar
            
        Returns:
            Lista de documentos relevantes con metadata
            
        Uso:
            Útil para previsualizar qué información se usará para responder,
            o para obtener contexto sin el costo de generar una respuesta LLM.
        """
        try:
            docs = self.retriever.get_relevant_documents(question)[:k]
            
            context = []
            for doc in docs:
                context.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })
            
            return context
            
        except Exception as e:
            logger.error(f"Error al obtener contexto: {str(e)}")
            return []
