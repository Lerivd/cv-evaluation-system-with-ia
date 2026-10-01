import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from models.cv_model import AnalisisCV
from prompts.cv_prompts import crear_sistema_prompts

load_dotenv()

class CVEvaluator:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        self.model_name = "gemini-2.5-flash"

    def _get_evaluation_chain(self):
        model = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=0.2,
            google_api_key=self.api_key
        )
        structured_model = model.with_structured_output(AnalisisCV)
        prompt = crear_sistema_prompts()
        return prompt | structured_model

    def evaluate(self, cv_text: str, job_description: str) -> AnalisisCV:
        try:
            chain = self._get_evaluation_chain()
            return chain.invoke({
                "texto_cv": cv_text,
                "descripcion_puesto": job_description
            })
        except Exception:
            return self._get_fallback_result()

    def _get_fallback_result(self) -> AnalisisCV:
        return AnalisisCV(
            nombre_candidato="Error processing candidate information.",
            experiencia_años=0,
            habilidades_clave=["Analysis error"],
            education="Undetermined",
            experiencia_relevante="Error during evaluation process.",
            fortalezas=["Manual review required"],
            areas_mejora=["Verify PDF format and legibility"],
            porcentaje_ajuste=0
        )

def evaluar_candidato(texto_cv: str, descripcion_puesto: str) -> AnalisisCV:
    try:
        evaluator = CVEvaluator()
        return evaluator.evaluate(texto_cv, descripcion_puesto)
    except Exception:
        # Fallback to empty result in case of initialization error (e.g., missing API key)
        return AnalisisCV(
            nombre_candidato="Configuration Error",
            experiencia_años=0,
            habilidades_clave=["Initialization error"],
            education="Undetermined",
            experiencia_relevante="Could not initialize AI service. Check API key configuration.",
            fortalezas=["Check .env file"],
            areas_mejora=["Ensure GOOGLE_API_KEY is set"],
            porcentaje_ajuste=0
        )
