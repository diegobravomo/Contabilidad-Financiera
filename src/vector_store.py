"""
Almacén Vectorial - Vector Store

Este módulo gestiona la base de datos vectorial ChromaDB para almacenar
y buscar embeddings de documentos contables.

Conceptos Contables Relacionados:
- Así como un sistema contable organiza información financiera para
  consultas eficientes, ChromaDB organiza información textual en vectores
  para búsquedas semánticas rápidas.
- La vectorización es análoga a la clasificación de cuentas contables:
  agrupa conceptos similares para facilitar su recuperación.
"""

from typing import List, Optional, Dict, Any, Tuple
import logging
from pathlib import Path

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStore:
    """
    Clase para gestionar el almacén vectorial de documentos contables.
    
    Esta clase implementa el patrón Repository para abstraer las operaciones
    de persistencia y recuperación de vectores de documentos.
    
    Atributos:
        persist_directory (str): Directorio donde se persiste la base de datos
        collection_name (str): Nombre de la colección en ChromaDB
        embeddings: Modelo de embeddings utilizado
        vector_store: Instancia de ChromaDB
    """
    
    def __init__(
        self,
        persist_directory: str,
        collection_name: str = "contabilidad_financiera",
        embedding_model: str = "text-embedding-ada-002"
    ):
        """
        Inicializa el almacén vectorial.
        
        Args:
            persist_directory: Directorio para persistir la base de datos
            collection_name: Nombre de la colección de ChromaDB
            embedding_model: Modelo de OpenAI para generar embeddings
            
        Nota Contable:
            La persistencia es crucial en contabilidad (principio de registro).
            De manera similar, persistimos los vectores para no tener que
            reprocesar documentos cada vez que se inicia la aplicación.
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Crear directorio si no existe
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Inicializar embeddings de OpenAI
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        
        # Inicializar o cargar el vector store
        self.vector_store: Optional[Chroma] = None
        
        logger.info(f"VectorStore inicializado en {persist_directory}")
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """
        Crea un nuevo almacén vectorial desde una lista de documentos.
        
        Args:
            documents: Lista de documentos a vectorizar
            
        Returns:
            Instancia de Chroma con los documentos indexados
            
        Raises:
            ValueError: Si la lista de documentos está vacía
            
        Concepto Contable:
            Similar al proceso de registro inicial de transacciones en un
            libro contable, este método "registra" los documentos en la
            base de datos vectorial por primera vez.
        """
        if not documents:
            logger.error("No se pueden crear vectores de una lista vacía de documentos")
            raise ValueError("La lista de documentos no puede estar vacía")
        
        try:
            logger.info(f"Creando almacén vectorial con {len(documents)} documentos...")
            
            # Crear el vector store con ChromaDB
            self.vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=self.collection_name,
                persist_directory=self.persist_directory
            )
            
            # Persistir los cambios
            self.vector_store.persist()
            
            logger.info("Almacén vectorial creado y persistido exitosamente")
            return self.vector_store
            
        except Exception as e:
            logger.error(f"Error al crear almacén vectorial: {str(e)}")
            raise
    
    def load_vector_store(self) -> Chroma:
        """
        Carga un almacén vectorial existente desde el disco.
        
        Returns:
            Instancia de Chroma cargada desde el directorio de persistencia
            
        Concepto Contable:
            Equivalente a abrir un libro contable existente para consultar
            información previamente registrada. No se crean nuevos registros,
            solo se accede a los existentes.
        """
        try:
            logger.info(f"Cargando almacén vectorial desde {self.persist_directory}")
            
            self.vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
            
            logger.info("Almacén vectorial cargado exitosamente")
            return self.vector_store
            
        except Exception as e:
            logger.error(f"Error al cargar almacén vectorial: {str(e)}")
            raise
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Añade nuevos documentos a un almacén vectorial existente.
        
        Args:
            documents: Lista de documentos a añadir
            
        Concepto Contable:
            Similar al asiento de ajuste o registro de nuevas transacciones
            en un período contable ya iniciado. Los nuevos documentos se
            "contabilizan" sin eliminar los registros anteriores.
        """
        if not self.vector_store:
            logger.warning("No hay almacén vectorial cargado. Creando uno nuevo...")
            self.create_vector_store(documents)
            return
        
        try:
            logger.info(f"Añadiendo {len(documents)} documentos al almacén vectorial...")
            
            self.vector_store.add_documents(documents)
            self.vector_store.persist()
            
            logger.info("Documentos añadidos y persistidos exitosamente")
            
        except Exception as e:
            logger.error(f"Error al añadir documentos: {str(e)}")
            raise
    
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Realiza una búsqueda de similitud en el almacén vectorial.
        
        Args:
            query: Texto de consulta
            k: Número de resultados a devolver
            filter: Filtros opcionales para la búsqueda
            
        Returns:
            Lista de documentos más similares a la consulta
            
        Concepto Contable:
            Análogo a buscar transacciones o conceptos específicos en registros
            contables. La búsqueda semántica encuentra información relacionada
            incluso si no hay coincidencia exacta de términos.
            
        Ejemplo:
            Si buscas "depreciación de activos", encontrará información sobre
            amortización, deterioro de activos, vida útil, etc.
        """
        if not self.vector_store:
            logger.error("No hay almacén vectorial cargado")
            raise ValueError("Debe cargar o crear un almacén vectorial primero")
        
        try:
            logger.info(f"Buscando: '{query}' (top {k} resultados)")
            
            results = self.vector_store.similarity_search(
                query=query,
                k=k,
                filter=filter
            )
            
            logger.info(f"Búsqueda completada: {len(results)} resultados encontrados")
            return results
            
        except Exception as e:
            logger.error(f"Error en búsqueda de similitud: {str(e)}")
            raise
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4
    ) -> List[Tuple[Document, float]]:
        """
        Realiza una búsqueda de similitud con puntuaciones.
        
        Args:
            query: Texto de consulta
            k: Número de resultados a devolver
            
        Returns:
            Lista de tuplas (documento, puntuación de similitud)
            
        Nota Contable:
            La puntuación de similitud es como el grado de certeza o
            confiabilidad en un análisis financiero. Valores más altos
            indican mayor relevancia del documento para la consulta.
        """
        if not self.vector_store:
            logger.error("No hay almacén vectorial cargado")
            raise ValueError("Debe cargar o crear un almacén vectorial primero")
        
        try:
            logger.info(f"Buscando con scores: '{query}' (top {k} resultados)")
            
            results = self.vector_store.similarity_search_with_score(query=query, k=k)
            
            logger.info(f"Búsqueda completada: {len(results)} resultados con scores")
            return results
            
        except Exception as e:
            logger.error(f"Error en búsqueda con scores: {str(e)}")
            raise
    
    def as_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        """
        Convierte el almacén vectorial en un retriever de LangChain.
        
        Args:
            search_kwargs: Argumentos de búsqueda opcionales
            
        Returns:
            Retriever configurado para usar en cadenas de LangChain
            
        Concepto Contable:
            Un retriever es como un sistema de consulta automatizado que
            busca información relevante. En contabilidad, sería equivalente
            a un sistema que busca automáticamente las normas o principios
            aplicables a una situación específica.
        """
        if not self.vector_store:
            logger.error("No hay almacén vectorial cargado")
            raise ValueError("Debe cargar o crear un almacén vectorial primero")
        
        if search_kwargs is None:
            search_kwargs = {"k": 4}
        
        logger.info(f"Creando retriever con kwargs: {search_kwargs}")
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)
    
    def get_collection_count(self) -> int:
        """
        Obtiene el número de documentos en la colección.
        
        Returns:
            Número de documentos en el almacén vectorial
            
        Concepto Contable:
            Similar a contar el número de asientos en un libro mayor o
            el número de transacciones registradas en un período.
        """
        if not self.vector_store:
            logger.warning("No hay almacén vectorial cargado")
            return 0
        
        try:
            count = self.vector_store._collection.count()
            logger.info(f"Documentos en la colección: {count}")
            return count
        except Exception as e:
            logger.error(f"Error al obtener conteo de colección: {str(e)}")
            return 0
    
    def delete_collection(self) -> None:
        """
        Elimina la colección completa del almacén vectorial.
        
        Advertencia:
            Esta operación es irreversible. Úsala con precaución.
            
        Concepto Contable:
            Equivalente al cierre y archivo de registros contables al final
            de un período, con la diferencia de que aquí los datos se eliminan
            completamente en lugar de archivarse.
        """
        if self.vector_store:
            try:
                logger.warning(f"Eliminando colección: {self.collection_name}")
                self.vector_store.delete_collection()
                self.vector_store = None
                logger.info("Colección eliminada exitosamente")
            except Exception as e:
                logger.error(f"Error al eliminar colección: {str(e)}")
                raise
        else:
            logger.warning("No hay almacén vectorial para eliminar")
