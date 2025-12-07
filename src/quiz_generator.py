"""
Generador de Quizzes - Quiz Generator

Este módulo implementa la generación automática de cuestionarios y
evaluaciones sobre conceptos contables.

Conceptos Contables Relacionados:
- Los quizzes son herramientas de evaluación educativa, similares a cómo
  las auditorías evalúan el conocimiento y aplicación de normas contables.
- La generación automática asegura cobertura amplia de temas, como un
  control interno bien diseñado cubre múltiples áreas de riesgo.
"""

from typing import List, Dict, Any, Optional
import logging
import json
import re

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuizQuestion:
    """
    Clase que representa una pregunta de quiz.
    
    Atributos:
        question: Texto de la pregunta
        options: Lista de opciones de respuesta
        correct_answer: Letra de la respuesta correcta (A, B, C, D)
        explanation: Explicación de por qué la respuesta es correcta
        topic: Tema contable relacionado
    """
    
    def __init__(
        self,
        question: str,
        options: List[str],
        correct_answer: str,
        explanation: str = "",
        topic: str = ""
    ):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer.upper()
        self.explanation = explanation
        self.topic = topic
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la pregunta a diccionario."""
        return {
            "question": self.question,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "topic": self.topic
        }
    
    def format_for_display(self, show_answer: bool = False) -> str:
        """
        Formatea la pregunta para mostrar al usuario.
        
        Args:
            show_answer: Si True, incluye la respuesta correcta y explicación
            
        Returns:
            String formateado de la pregunta
        """
        formatted = f"**{self.question}**\n\n"
        
        for i, option in enumerate(self.options):
            letter = chr(65 + i)  # A, B, C, D...
            formatted += f"{letter}) {option}\n"
        
        if show_answer:
            formatted += f"\n**Respuesta correcta:** {self.correct_answer}\n"
            if self.explanation:
                formatted += f"**Explicación:** {self.explanation}\n"
        
        return formatted


class QuizGenerator:
    """
    Generador de cuestionarios sobre contabilidad financiera.
    
    Esta clase genera automáticamente preguntas de opción múltiple
    basadas en contenido contable proporcionado.
    
    Atributos:
        llm: Modelo de lenguaje para generación de preguntas
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7
    ):
        """
        Inicializa el generador de quizzes.
        
        Args:
            model_name: Nombre del modelo de OpenAI
            temperature: Temperatura del modelo (0-1)
            
        Nota Contable:
            Usamos temperatura moderada (0.7) para balance entre preguntas
            predecibles y variedad. Similar a cómo un examen contable debe
            ser justo pero desafiante.
        """
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature
        )
        
        logger.info(f"QuizGenerator inicializado con modelo {model_name}")
    
    def _get_quiz_prompt(self, num_questions: int, difficulty: str = "medium") -> PromptTemplate:
        """
        Crea el prompt para generación de preguntas.
        
        Args:
            num_questions: Número de preguntas a generar
            difficulty: Nivel de dificultad (easy, medium, hard)
            
        Returns:
            PromptTemplate configurado
            
        Concepto Contable:
            El prompt define los criterios de calidad del quiz, similar a
            cómo las normas de auditoría establecen criterios para evaluar
            la evidencia contable.
        """
        difficulty_guide = {
            "easy": "básicas, de comprensión directa",
            "medium": "de comprensión y aplicación moderada",
            "hard": "complejas, que requieren análisis y síntesis"
        }
        
        level = difficulty_guide.get(difficulty, difficulty_guide["medium"])
        
        template = f"""Basándote en el siguiente contenido sobre contabilidad financiera, genera {num_questions} preguntas de opción múltiple.

Requisitos:
1. Nivel de dificultad: {level}
2. Cada pregunta debe tener exactamente 4 opciones (A, B, C, D)
3. Solo una respuesta debe ser correcta
4. Las opciones incorrectas deben ser plausibles pero claramente equivocadas
5. Incluye una explicación breve de por qué la respuesta es correcta
6. Las preguntas deben evaluar comprensión de conceptos contables importantes
7. Usa terminología contable apropiada

FORMATO REQUERIDO (sigue exactamente este formato):
Pregunta 1: [texto de la pregunta]
A) [opción A]
B) [opción B]
C) [opción C]
D) [opción D]
Respuesta correcta: [letra]
Explicación: [explicación]
Tema: [tema contable]

Pregunta 2: ...

Contenido:
{{text}}

Preguntas:"""
        
        return PromptTemplate(template=template, input_variables=["text"])
    
    def generate_quiz(
        self,
        text: str,
        num_questions: int = 5,
        difficulty: str = "medium"
    ) -> List[QuizQuestion]:
        """
        Genera un quiz basado en un texto sobre contabilidad.
        
        Args:
            text: Contenido contable de referencia
            num_questions: Número de preguntas a generar
            difficulty: Nivel de dificultad (easy, medium, hard)
            
        Returns:
            Lista de objetos QuizQuestion
            
        Ejemplo de Uso:
            >>> generator = QuizGenerator()
            >>> texto = "La depreciación es la distribución sistemática..."
            >>> quiz = generator.generate_quiz(texto, num_questions=3)
            >>> for q in quiz:
            ...     print(q.format_for_display())
            
        Concepto Contable:
            Genera evaluaciones automáticas similar a cómo se generan
            reportes de control de calidad o listas de verificación
            contable automáticas.
        """
        if not text or not text.strip():
            logger.warning("Texto vacío para generar quiz")
            return []
        
        if num_questions < 1:
            logger.warning("Número de preguntas debe ser al menos 1")
            num_questions = 1
        
        try:
            logger.info(f"Generando quiz: {num_questions} preguntas, nivel {difficulty}")
            
            # Limitar el texto si es muy largo
            max_text_length = 3000
            if len(text) > max_text_length:
                text = text[:max_text_length] + "..."
                logger.info(f"Texto truncado a {max_text_length} caracteres")
            
            # Generar preguntas
            prompt = self._get_quiz_prompt(num_questions, difficulty)
            formatted_prompt = prompt.format(text=text)
            
            response = self.llm.predict(formatted_prompt)
            
            # Parsear respuesta
            questions = self._parse_quiz_response(response)
            
            logger.info(f"Quiz generado: {len(questions)} preguntas")
            return questions
            
        except Exception as e:
            logger.error(f"Error al generar quiz: {str(e)}")
            return []
    
    def _parse_quiz_response(self, response: str) -> List[QuizQuestion]:
        """
        Parsea la respuesta del LLM en objetos QuizQuestion.
        
        Args:
            response: Respuesta cruda del LLM
            
        Returns:
            Lista de objetos QuizQuestion
        """
        questions = []
        
        try:
            # Dividir por "Pregunta N:"
            question_blocks = re.split(r'Pregunta \d+:', response)
            
            for block in question_blocks[1:]:  # Saltar el primer elemento vacío
                if not block.strip():
                    continue
                
                lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
                
                if len(lines) < 6:  # Necesitamos al menos pregunta + 4 opciones + respuesta
                    continue
                
                # Extraer pregunta
                question_text = lines[0]
                
                # Extraer opciones
                options = []
                correct_answer = ""
                explanation = ""
                topic = ""
                
                for line in lines[1:]:
                    if line.startswith(('A)', 'B)', 'C)', 'D)')):
                        option = line[3:].strip()
                        options.append(option)
                    elif line.startswith('Respuesta correcta:'):
                        correct_answer = line.replace('Respuesta correcta:', '').strip()
                        # Extraer solo la letra
                        correct_answer = re.search(r'[A-D]', correct_answer)
                        if correct_answer:
                            correct_answer = correct_answer.group()
                    elif line.startswith('Explicación:'):
                        explanation = line.replace('Explicación:', '').strip()
                    elif line.startswith('Tema:'):
                        topic = line.replace('Tema:', '').strip()
                
                # Validar que tenemos datos completos
                if question_text and len(options) == 4 and correct_answer:
                    quiz_question = QuizQuestion(
                        question=question_text,
                        options=options,
                        correct_answer=correct_answer,
                        explanation=explanation,
                        topic=topic
                    )
                    questions.append(quiz_question)
            
        except Exception as e:
            logger.error(f"Error al parsear respuesta de quiz: {str(e)}")
        
        return questions
    
    def generate_quiz_from_documents(
        self,
        documents: List[Document],
        num_questions: int = 5,
        difficulty: str = "medium"
    ) -> List[QuizQuestion]:
        """
        Genera un quiz basado en múltiples documentos.
        
        Args:
            documents: Lista de documentos de LangChain
            num_questions: Número total de preguntas
            difficulty: Nivel de dificultad
            
        Returns:
            Lista de objetos QuizQuestion
            
        Concepto Contable:
            Similar a generar un examen comprensivo que cubre múltiples
            temas contables (activos, pasivos, patrimonio, etc.) de manera
            integrada.
        """
        if not documents:
            logger.warning("Lista de documentos vacía")
            return []
        
        try:
            # Combinar contenido de documentos
            combined_text = "\n\n".join([doc.page_content for doc in documents])
            
            # Generar quiz del texto combinado
            return self.generate_quiz(combined_text, num_questions, difficulty)
            
        except Exception as e:
            logger.error(f"Error al generar quiz de documentos: {str(e)}")
            return []
    
    def check_answer(
        self,
        question: QuizQuestion,
        user_answer: str
    ) -> Dict[str, Any]:
        """
        Verifica si la respuesta del usuario es correcta.
        
        Args:
            question: Objeto QuizQuestion
            user_answer: Respuesta del usuario (A, B, C, o D)
            
        Returns:
            Diccionario con resultado y feedback
            
        Concepto Contable:
            Similar a verificar si un asiento contable es correcto comparando
            con las normas y principios aplicables.
        """
        user_answer = user_answer.upper().strip()
        
        is_correct = user_answer == question.correct_answer
        
        result = {
            "is_correct": is_correct,
            "user_answer": user_answer,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation
        }
        
        if is_correct:
            result["feedback"] = "¡Correcto! " + question.explanation
        else:
            result["feedback"] = f"Incorrecto. La respuesta correcta es {question.correct_answer}. {question.explanation}"
        
        return result
    
    def score_quiz(
        self,
        questions: List[QuizQuestion],
        user_answers: List[str]
    ) -> Dict[str, Any]:
        """
        Califica un quiz completo.
        
        Args:
            questions: Lista de preguntas del quiz
            user_answers: Lista de respuestas del usuario (mismo orden)
            
        Returns:
            Diccionario con puntuación y análisis
            
        Concepto Contable:
            Similar a calcular ratios financieros o indicadores de desempeño.
            La puntuación proporciona una medida cuantitativa del rendimiento.
        """
        if len(questions) != len(user_answers):
            logger.error("Número de preguntas y respuestas no coinciden")
            return {
                "error": "El número de preguntas y respuestas debe coincidir",
                "score": 0,
                "percentage": 0
            }
        
        correct_count = 0
        total = len(questions)
        results = []
        
        for i, (question, answer) in enumerate(zip(questions, user_answers), 1):
            result = self.check_answer(question, answer)
            result["question_number"] = i
            result["question_text"] = question.question
            results.append(result)
            
            if result["is_correct"]:
                correct_count += 1
        
        percentage = (correct_count / total * 100) if total > 0 else 0
        
        # Determinar calificación cualitativa
        if percentage >= 90:
            grade = "Excelente"
        elif percentage >= 80:
            grade = "Muy Bien"
        elif percentage >= 70:
            grade = "Bien"
        elif percentage >= 60:
            grade = "Aprobado"
        else:
            grade = "Necesita mejorar"
        
        return {
            "total_questions": total,
            "correct_answers": correct_count,
            "incorrect_answers": total - correct_count,
            "score": correct_count,
            "percentage": round(percentage, 2),
            "grade": grade,
            "results": results
        }
    
    def export_quiz_to_json(
        self,
        questions: List[QuizQuestion],
        filename: str
    ) -> bool:
        """
        Exporta un quiz a formato JSON.
        
        Args:
            questions: Lista de preguntas
            filename: Nombre del archivo de salida
            
        Returns:
            True si exitoso, False en caso contrario
            
        Concepto Contable:
            Similar a exportar información contable a formatos estándar
            (XML, CSV) para intercambio o archivo.
        """
        try:
            quiz_data = {
                "total_questions": len(questions),
                "questions": [q.to_dict() for q in questions]
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(quiz_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Quiz exportado a {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error al exportar quiz: {str(e)}")
            return False
