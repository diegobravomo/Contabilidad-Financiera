"""
Generador de Resúmenes - Summary Generator

Este módulo implementa la generación automática de resúmenes de
documentos y conceptos contables utilizando LLMs.

Conceptos Contables Relacionados:
- Los resúmenes son como las notas a los estados financieros: condensan
  información compleja en formatos más digeribles sin perder lo esencial.
- Similar a un informe ejecutivo que presenta los puntos clave de un
  análisis financiero extenso.
"""

from typing import List, Optional, Dict, Any
import logging

from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SummaryGenerator:
    """
    Generador de resúmenes para contenido contable.
    
    Esta clase proporciona diferentes estrategias de resumen según la
    longitud y complejidad del contenido a resumir.
    
    Atributos:
        llm: Modelo de lenguaje para generación de resúmenes
        text_splitter: Divisor de texto para documentos largos
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.3
    ):
        """
        Inicializa el generador de resúmenes.
        
        Args:
            model_name: Nombre del modelo de OpenAI
            temperature: Temperatura del modelo (0-1)
            
        Nota Contable:
            Usamos temperatura baja (0.3) para resúmenes porque queremos
            precisión y consistencia, similar a cómo los informes financieros
            requieren exactitud sobre creatividad.
        """
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=200
        )
        
        logger.info(f"SummaryGenerator inicializado con modelo {model_name}")
    
    def _get_summary_prompt(self) -> PromptTemplate:
        """
        Crea el prompt para generación de resúmenes.
        
        Returns:
            PromptTemplate configurado para resúmenes contables
            
        Concepto Contable:
            El prompt guía la estructura del resumen, similar a cómo
            las normas contables establecen la estructura de los informes
            financieros (qué incluir, en qué orden, con qué nivel de detalle).
        """
        template = """Resume el siguiente texto sobre contabilidad financiera de manera clara y estructurada.

Instrucciones:
1. Identifica los conceptos contables clave
2. Destaca definiciones y principios importantes
3. Organiza la información en puntos principales
4. Mantén la terminología técnica contable apropiada
5. Incluye ejemplos relevantes si los hay
6. Asegúrate de que el resumen sea comprensible para estudiantes

Texto:
{text}

RESUMEN ESTRUCTURADO:"""
        
        return PromptTemplate(template=template, input_variables=["text"])
    
    def _get_refine_prompt(self) -> tuple[PromptTemplate, PromptTemplate]:
        """
        Crea prompts para el método de refinamiento.
        
        Returns:
            Tupla con (prompt_inicial, prompt_refinamiento)
            
        Concepto Contable:
            El refinamiento es como el proceso de ajustes y reclasificaciones
            contables: comenzamos con un borrador y lo mejoramos iterativamente
            hasta obtener un resultado preciso y completo.
        """
        # Prompt inicial
        initial_template = """Resume el siguiente texto de contabilidad de manera concisa:

{text}

RESUMEN:"""
        initial_prompt = PromptTemplate(
            template=initial_template,
            input_variables=["text"]
        )
        
        # Prompt de refinamiento
        refine_template = """Tu tarea es producir un resumen final mejorado.
Ya tenemos un resumen parcial: {existing_answer}

Ahora, refina el resumen incorporando el siguiente texto adicional:
{text}

Produce un resumen mejorado que integre toda la información relevante.
Mantén la estructura clara y enfócate en conceptos contables importantes.

RESUMEN REFINADO:"""
        refine_prompt = PromptTemplate(
            template=refine_template,
            input_variables=["existing_answer", "text"]
        )
        
        return initial_prompt, refine_prompt
    
    def generate_summary(
        self,
        text: str,
        max_length: Optional[int] = None
    ) -> str:
        """
        Genera un resumen de un texto sobre contabilidad.
        
        Args:
            text: Texto a resumir
            max_length: Longitud máxima aproximada del resumen (opcional)
            
        Returns:
            Resumen generado
            
        Ejemplo de Uso:
            >>> generator = SummaryGenerator()
            >>> texto = "La depreciación es la asignación sistemática..."
            >>> resumen = generator.generate_summary(texto)
            >>> print(resumen)
            
        Concepto Contable:
            Genera resúmenes ejecutivos de conceptos contables, similar a
            cómo un contador prepara un resumen de políticas contables o
            un extracto de una norma NIIF para presentación a gerencia.
        """
        if not text or not text.strip():
            logger.warning("Texto vacío para resumir")
            return "No se proporcionó texto para resumir."
        
        try:
            logger.info(f"Generando resumen de texto ({len(text)} caracteres)...")
            
            # Para textos cortos, usar método directo
            if len(text) < 4000:
                return self._summarize_short_text(text)
            else:
                # Para textos largos, usar método de refinamiento
                return self._summarize_long_text(text)
                
        except Exception as e:
            logger.error(f"Error al generar resumen: {str(e)}")
            return f"Error al generar resumen: {str(e)}"
    
    def _summarize_short_text(self, text: str) -> str:
        """
        Resume texto corto en una sola llamada al LLM.
        
        Args:
            text: Texto a resumir (menos de 4000 caracteres)
            
        Returns:
            Resumen generado
        """
        try:
            prompt = self._get_summary_prompt()
            formatted_prompt = prompt.format(text=text)
            
            response = self.llm.predict(formatted_prompt)
            
            logger.info("Resumen de texto corto generado exitosamente")
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error en resumen corto: {str(e)}")
            raise
    
    def _summarize_long_text(self, text: str) -> str:
        """
        Resume texto largo usando el método de refinamiento.
        
        Args:
            text: Texto largo a resumir
            
        Returns:
            Resumen generado
            
        Concepto Contable:
            El método de refinamiento es como consolidar múltiples estados
            financieros: procesamos cada parte individualmente y luego
            integramos todo en un resumen coherente final.
        """
        try:
            # Dividir el texto en chunks
            docs = [Document(page_content=text)]
            split_docs = self.text_splitter.split_documents(docs)
            
            logger.info(f"Texto dividido en {len(split_docs)} fragmentos para resumen")
            
            # Obtener prompts
            initial_prompt, refine_prompt = self._get_refine_prompt()
            
            # Crear cadena de resumen con refinamiento
            chain = load_summarize_chain(
                llm=self.llm,
                chain_type="refine",
                question_prompt=initial_prompt,
                refine_prompt=refine_prompt,
                return_intermediate_steps=False
            )
            
            # Generar resumen
            result = chain({"input_documents": split_docs})
            
            logger.info("Resumen de texto largo generado exitosamente")
            return result["output_text"].strip()
            
        except Exception as e:
            logger.error(f"Error en resumen largo: {str(e)}")
            raise
    
    def summarize_documents(
        self,
        documents: List[Document],
        combine: bool = True
    ) -> str:
        """
        Resume una lista de documentos.
        
        Args:
            documents: Lista de documentos de LangChain
            combine: Si True, genera un resumen combinado; si False, resúmenes separados
            
        Returns:
            Resumen de los documentos
            
        Concepto Contable:
            Similar a preparar un informe consolidado de múltiples subsidiarias
            (combine=True) o informes individuales por cada subsidiaria (combine=False).
        """
        if not documents:
            logger.warning("Lista de documentos vacía")
            return "No se proporcionaron documentos para resumir."
        
        try:
            logger.info(f"Resumiendo {len(documents)} documentos (combine={combine})...")
            
            if combine:
                # Combinar contenido de todos los documentos
                combined_text = "\n\n".join([doc.page_content for doc in documents])
                return self.generate_summary(combined_text)
            else:
                # Generar resumen individual para cada documento
                summaries = []
                for i, doc in enumerate(documents, 1):
                    summary = self.generate_summary(doc.page_content)
                    summaries.append(f"**Documento {i}:**\n{summary}")
                
                return "\n\n---\n\n".join(summaries)
                
        except Exception as e:
            logger.error(f"Error al resumir documentos: {str(e)}")
            return f"Error al resumir documentos: {str(e)}"
    
    def generate_key_points(self, text: str, num_points: int = 5) -> List[str]:
        """
        Extrae los puntos clave de un texto contable.
        
        Args:
            text: Texto a analizar
            num_points: Número de puntos clave a extraer
            
        Returns:
            Lista de puntos clave
            
        Concepto Contable:
            Similar a identificar los indicadores financieros clave (KPIs)
            o los aspectos más relevantes en un análisis financiero.
        """
        if not text or not text.strip():
            logger.warning("Texto vacío para extraer puntos clave")
            return []
        
        try:
            prompt = f"""Extrae los {num_points} puntos clave más importantes del siguiente texto sobre contabilidad.
Presenta cada punto como una oración concisa y clara.

Texto:
{text[:3000]}

Lista de {num_points} puntos clave:"""
            
            response = self.llm.predict(prompt)
            
            # Parsear la respuesta en lista
            points = []
            for line in response.strip().split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                    # Limpiar numeración o viñetas
                    clean_line = line.lstrip('0123456789.-•) ').strip()
                    if clean_line:
                        points.append(clean_line)
            
            logger.info(f"Extraídos {len(points)} puntos clave")
            return points[:num_points]
            
        except Exception as e:
            logger.error(f"Error al extraer puntos clave: {str(e)}")
            return []
    
    def generate_concept_map(self, text: str) -> Dict[str, Any]:
        """
        Genera un mapa conceptual simplificado del texto.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con estructura de conceptos principales y relacionados
            
        Concepto Contable:
            Un mapa conceptual es como el plan de cuentas contable:
            organiza conceptos en jerarquías y muestra relaciones entre ellos.
        """
        if not text or not text.strip():
            return {"main_concept": "N/A", "related_concepts": []}
        
        try:
            prompt = f"""Analiza el siguiente texto contable e identifica:
1. El concepto principal
2. Hasta 5 conceptos relacionados importantes

Formato de respuesta:
CONCEPTO PRINCIPAL: [concepto]
CONCEPTOS RELACIONADOS:
- [concepto 1]
- [concepto 2]
...

Texto:
{text[:2000]}

Análisis:"""
            
            response = self.llm.predict(prompt)
            
            # Parsear respuesta
            lines = response.strip().split('\n')
            main_concept = "No identificado"
            related_concepts = []
            
            parsing_related = False
            for line in lines:
                line = line.strip()
                if line.startswith("CONCEPTO PRINCIPAL:"):
                    main_concept = line.replace("CONCEPTO PRINCIPAL:", "").strip()
                elif line.startswith("CONCEPTOS RELACIONADOS:"):
                    parsing_related = True
                elif parsing_related and line.startswith('-'):
                    concept = line.lstrip('- ').strip()
                    if concept:
                        related_concepts.append(concept)
            
            return {
                "main_concept": main_concept,
                "related_concepts": related_concepts
            }
            
        except Exception as e:
            logger.error(f"Error al generar mapa conceptual: {str(e)}")
            return {"main_concept": "Error", "related_concepts": []}
