"""
Script de Ingesta de Documentos - ingest.py

Este script procesa documentos PDF sobre contabilidad financiera,
los vectoriza y los almacena en ChromaDB para búsquedas posteriores.

Conceptos Contables Relacionados:
- El proceso de ingesta es análogo al registro inicial de información
  en un sistema contable: toma datos en bruto (documentos) y los
  estructura en un formato útil para consultas futuras (vectores).
- Como el principio de registro contable, aseguramos que toda la
  información se capture de manera completa y estructurada.

Uso:
    python ingest.py [ruta_documentos]
    
Ejemplos:
    python ingest.py data/niif.pdf          # Procesar un solo archivo
    python ingest.py data/                  # Procesar todo un directorio
"""

import sys
import os
from pathlib import Path
import argparse
import logging
from dotenv import load_dotenv

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from config.settings import (
    CHROMA_PERSIST_DIRECTORY,
    CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    DATA_DIR
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DocumentIngestor:
    """
    Clase principal para la ingesta de documentos contables.
    
    Esta clase coordina el proceso completo de carga, procesamiento
    y vectorización de documentos.
    
    Concepto Contable:
        Actúa como el "departamento de contabilidad" que recibe,
        procesa y registra la información financiera de manera
        sistemática y organizada.
    """
    
    def __init__(self):
        """
        Inicializa el ingestor de documentos.
        
        Carga variables de entorno y verifica configuración necesaria.
        """
        # Cargar variables de entorno
        load_dotenv()
        
        # Verificar que existe la API key de OpenAI
        if not os.getenv("OPENAI_API_KEY"):
            logger.error("OPENAI_API_KEY no está configurada en el entorno")
            raise ValueError(
                "Por favor, configura OPENAI_API_KEY en un archivo .env o como variable de entorno"
            )
        
        # Inicializar procesador de documentos
        self.processor = DocumentProcessor(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        
        # Inicializar almacén vectorial
        self.vector_store_manager = VectorStore(
            persist_directory=CHROMA_PERSIST_DIRECTORY,
            collection_name=CHROMA_COLLECTION_NAME,
            embedding_model=EMBEDDING_MODEL
        )
        
        logger.info("DocumentIngestor inicializado correctamente")
    
    def ingest(self, source_path: str, force_recreate: bool = False) -> bool:
        """
        Procesa e ingesta documentos desde una ruta.
        
        Args:
            source_path: Ruta a archivo o directorio con PDFs
            force_recreate: Si True, elimina y recrea el almacén vectorial
            
        Returns:
            True si exitoso, False en caso contrario
            
        Concepto Contable:
            El proceso de ingesta sigue el ciclo contable:
            1. Identificar documentos (identificar transacciones)
            2. Procesar y dividir (analizar transacciones)
            3. Vectorizar (clasificar en cuentas)
            4. Almacenar (registrar en libros)
        """
        try:
            # Validar que la ruta existe
            source_path_obj = Path(source_path)
            if not source_path_obj.exists():
                logger.error(f"La ruta {source_path} no existe")
                return False
            
            logger.info("="*60)
            logger.info("INICIANDO PROCESO DE INGESTA DE DOCUMENTOS")
            logger.info("="*60)
            
            # Paso 1: Procesar documentos
            logger.info("\n[1/4] Procesando documentos...")
            documents = self.processor.process_documents(source_path)
            
            if not documents:
                logger.error("No se pudieron procesar documentos")
                return False
            
            logger.info(f"✓ Procesados {len(documents)} fragmentos de documentos")
            
            # Mostrar metadata
            metadata = self.processor.get_document_metadata(documents)
            logger.info(f"\nMetadata de documentos:")
            logger.info(f"  - Fuentes: {len(metadata['sources'])}")
            for source in metadata['sources']:
                logger.info(f"    • {Path(source).name}")
            logger.info(f"  - Total fragmentos: {metadata['total_documents']}")
            logger.info(f"  - Tamaño de fragmento: {metadata['chunk_size']} caracteres")
            logger.info(f"  - Solapamiento: {metadata['chunk_overlap']} caracteres")
            
            # Paso 2: Preparar almacén vectorial
            logger.info("\n[2/4] Preparando almacén vectorial...")
            
            # Verificar si existe ya un almacén
            vector_store_exists = Path(CHROMA_PERSIST_DIRECTORY).exists()
            
            if force_recreate and vector_store_exists:
                logger.warning("Eliminando almacén vectorial existente...")
                self.vector_store_manager.load_vector_store()
                self.vector_store_manager.delete_collection()
                logger.info("✓ Almacén vectorial eliminado")
            
            # Paso 3: Vectorizar y almacenar
            logger.info("\n[3/4] Vectorizando documentos...")
            logger.info("(Este proceso puede tomar varios minutos...)")
            
            if not vector_store_exists or force_recreate:
                # Crear nuevo almacén
                self.vector_store_manager.create_vector_store(documents)
                logger.info("✓ Almacén vectorial creado exitosamente")
            else:
                # Añadir a almacén existente
                logger.info("Almacén vectorial existente detectado")
                self.vector_store_manager.load_vector_store()
                logger.info("Añadiendo documentos al almacén existente...")
                self.vector_store_manager.add_documents(documents)
                logger.info("✓ Documentos añadidos al almacén vectorial")
            
            # Paso 4: Verificación
            logger.info("\n[4/4] Verificando ingesta...")
            doc_count = self.vector_store_manager.get_collection_count()
            logger.info(f"✓ Almacén vectorial contiene {doc_count} documentos")
            
            # Resumen final
            logger.info("\n" + "="*60)
            logger.info("INGESTA COMPLETADA EXITOSAMENTE")
            logger.info("="*60)
            logger.info(f"\nResumen:")
            logger.info(f"  • Documentos procesados: {len(metadata['sources'])}")
            logger.info(f"  • Fragmentos generados: {len(documents)}")
            logger.info(f"  • Documentos en BD vectorial: {doc_count}")
            logger.info(f"  • Ubicación: {CHROMA_PERSIST_DIRECTORY}")
            logger.info(f"\nLos documentos están listos para consultas en la aplicación.")
            
            return True
            
        except Exception as e:
            logger.error(f"Error durante la ingesta: {str(e)}", exc_info=True)
            return False
    
    def list_ingested_sources(self) -> list:
        """
        Lista las fuentes de documentos ya ingestadas.
        
        Returns:
            Lista de nombres de archivos fuente
            
        Concepto Contable:
            Similar a listar los libros contables o fuentes de
            información que están disponibles en el sistema.
        """
        try:
            # Intentar cargar el almacén vectorial
            if not Path(CHROMA_PERSIST_DIRECTORY).exists():
                logger.info("No existe almacén vectorial todavía")
                return []
            
            self.vector_store_manager.load_vector_store()
            
            # Obtener información de la colección
            doc_count = self.vector_store_manager.get_collection_count()
            
            logger.info(f"Almacén vectorial contiene {doc_count} documentos")
            
            return []  # ChromaDB no proporciona fácilmente lista de fuentes únicas
            
        except Exception as e:
            logger.error(f"Error al listar fuentes: {str(e)}")
            return []


def main():
    """
    Función principal del script.
    
    Maneja argumentos de línea de comandos y ejecuta la ingesta.
    """
    parser = argparse.ArgumentParser(
        description="Procesa e ingesta documentos PDF de contabilidad financiera",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Procesar un solo archivo PDF
  python ingest.py data/niif_9.pdf
  
  # Procesar todos los PDFs en un directorio
  python ingest.py data/
  
  # Forzar recreación del almacén vectorial
  python ingest.py data/ --force-recreate
  
  # Listar fuentes ingestadas
  python ingest.py --list

Notas:
  - Asegúrate de tener OPENAI_API_KEY configurada en tu entorno
  - Los documentos se almacenan en la base de datos ChromaDB
  - El proceso de vectorización puede tomar varios minutos
        """
    )
    
    parser.add_argument(
        'path',
        type=str,
        nargs='?',
        default=str(DATA_DIR),
        help='Ruta al archivo PDF o directorio con PDFs (por defecto: data/)'
    )
    
    parser.add_argument(
        '--force-recreate',
        '-f',
        action='store_true',
        help='Eliminar y recrear el almacén vectorial'
    )
    
    parser.add_argument(
        '--list',
        '-l',
        action='store_true',
        help='Listar documentos ya ingestados'
    )
    
    args = parser.parse_args()
    
    try:
        # Crear ingestor
        ingestor = DocumentIngestor()
        
        # Listar si se solicita
        if args.list:
            logger.info("Documentos ingestados:")
            sources = ingestor.list_ingested_sources()
            if not sources:
                logger.info("  (Usa el almacén vectorial, no hay lista específica disponible)")
            sys.exit(0)
        
        # Ejecutar ingesta
        success = ingestor.ingest(args.path, force_recreate=args.force_recreate)
        
        if success:
            logger.info("\n✓ Proceso completado exitosamente")
            sys.exit(0)
        else:
            logger.error("\n✗ El proceso falló")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("\n\nProceso interrumpido por el usuario")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\nError fatal: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
