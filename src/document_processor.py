"""
Procesador de Documentos - Document Processor

Este módulo contiene la clase DocumentProcessor que se encarga de cargar,
procesar y dividir documentos PDF para su posterior vectorización.

Conceptos Contables Relacionados:
- Los documentos pueden contener información sobre NIIF (Normas Internacionales
  de Información Financiera), estados financieros, principios contables, etc.
- El procesamiento adecuado de estos documentos es crucial para mantener la
  integridad de la información contable y permitir consultas precisas.
"""

from typing import List, Optional
from pathlib import Path
import logging

from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Clase para procesar documentos PDF relacionados con Contabilidad Financiera.
    
    Esta clase implementa el patrón de diseño Strategy para permitir diferentes
    métodos de carga y procesamiento de documentos según el tipo de archivo.
    
    Atributos:
        chunk_size (int): Tamaño de los fragmentos de texto en caracteres
        chunk_overlap (int): Solapamiento entre fragmentos consecutivos
        text_splitter (RecursiveCharacterTextSplitter): Divisor de texto configurado
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Inicializa el procesador de documentos.
        
        Args:
            chunk_size: Tamaño de cada fragmento de texto (por defecto 1000 caracteres)
            chunk_overlap: Número de caracteres que se solapan entre fragmentos (por defecto 200)
        
        Nota Contable:
            El tamaño del fragmento debe ser lo suficientemente grande para mantener
            el contexto de conceptos contables complejos, pero lo suficientemente
            pequeño para búsquedas eficientes.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        logger.info(f"DocumentProcessor inicializado con chunk_size={chunk_size}, overlap={chunk_overlap}")
    
    def load_pdf(self, file_path: str) -> List[Document]:
        """
        Carga un archivo PDF individual.
        
        Args:
            file_path: Ruta al archivo PDF
            
        Returns:
            Lista de objetos Document de LangChain
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            Exception: Si hay un error al cargar el PDF
            
        Ejemplo de Uso:
            >>> processor = DocumentProcessor()
            >>> docs = processor.load_pdf("data/niif_9.pdf")
            >>> print(f"Cargadas {len(docs)} páginas de NIIF 9")
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.error(f"Archivo no encontrado: {file_path}")
            raise FileNotFoundError(f"El archivo {file_path} no existe")
        
        try:
            logger.info(f"Cargando PDF: {file_path}")
            loader = PyPDFLoader(str(file_path))
            documents = loader.load()
            logger.info(f"PDF cargado exitosamente: {len(documents)} páginas")
            return documents
        except Exception as e:
            logger.error(f"Error al cargar PDF {file_path}: {str(e)}")
            raise
    
    def load_directory(self, directory_path: str) -> List[Document]:
        """
        Carga todos los archivos PDF de un directorio.
        
        Args:
            directory_path: Ruta al directorio que contiene PDFs
            
        Returns:
            Lista de todos los documentos cargados
            
        Nota Contable:
            Útil para cargar múltiples documentos como varias NIIF,
            diferentes capítulos de libros contables, o material de estudio variado.
        """
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            logger.error(f"Directorio no encontrado: {directory_path}")
            raise FileNotFoundError(f"El directorio {directory_path} no existe")
        
        try:
            logger.info(f"Cargando PDFs del directorio: {directory_path}")
            loader = DirectoryLoader(
                str(directory_path),
                glob="**/*.pdf",
                loader_cls=PyPDFLoader
            )
            documents = loader.load()
            logger.info(f"Directorio cargado: {len(documents)} páginas totales")
            return documents
        except Exception as e:
            logger.error(f"Error al cargar directorio {directory_path}: {str(e)}")
            raise
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Divide documentos en fragmentos más pequeños para procesamiento.
        
        Args:
            documents: Lista de documentos a dividir
            
        Returns:
            Lista de documentos divididos en fragmentos
            
        Concepto Contable:
            Similar a cómo la información financiera se organiza en secciones
            (Balance General, Estado de Resultados, Notas), dividimos los documentos
            en fragmentos manejables que preservan el contexto contable relevante.
        """
        if not documents:
            logger.warning("No hay documentos para dividir")
            return []
        
        try:
            logger.info(f"Dividiendo {len(documents)} documentos...")
            split_docs = self.text_splitter.split_documents(documents)
            logger.info(f"Documentos divididos en {len(split_docs)} fragmentos")
            return split_docs
        except Exception as e:
            logger.error(f"Error al dividir documentos: {str(e)}")
            raise
    
    def process_documents(self, source_path: str) -> List[Document]:
        """
        Método principal que carga y procesa documentos desde un archivo o directorio.
        
        Args:
            source_path: Ruta a un archivo PDF o directorio
            
        Returns:
            Lista de documentos procesados y divididos
            
        Ejemplo de Uso:
            >>> processor = DocumentProcessor()
            >>> docs = processor.process_documents("data/")
            >>> print(f"Procesados {len(docs)} fragmentos de documentos contables")
        """
        source_path = Path(source_path)
        
        # Determinar si es un archivo o directorio
        if source_path.is_file():
            documents = self.load_pdf(str(source_path))
        elif source_path.is_dir():
            documents = self.load_directory(str(source_path))
        else:
            raise ValueError(f"{source_path} no es un archivo ni directorio válido")
        
        # Dividir documentos en fragmentos
        split_docs = self.split_documents(documents)
        
        logger.info(f"Procesamiento completo: {len(split_docs)} fragmentos listos para vectorización")
        return split_docs
    
    def get_document_metadata(self, documents: List[Document]) -> dict:
        """
        Extrae metadata útil de los documentos procesados.
        
        Args:
            documents: Lista de documentos
            
        Returns:
            Diccionario con estadísticas de los documentos
            
        Nota Contable:
            Similar a las notas explicativas en estados financieros,
            esta metadata proporciona información contextual importante.
        """
        if not documents:
            return {"total_documents": 0, "total_pages": 0, "sources": []}
        
        sources = set()
        total_pages = 0
        
        for doc in documents:
            if hasattr(doc, 'metadata'):
                source = doc.metadata.get('source', 'unknown')
                sources.add(source)
                total_pages += 1
        
        return {
            "total_documents": len(documents),
            "total_pages": total_pages,
            "sources": list(sources),
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap
        }
