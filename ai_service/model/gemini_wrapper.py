# ai_service/gemini_wrapper.py
import os
import logging
from typing import Optional
from dotenv import load_dotenv
import importlib

logger = logging.getLogger(__name__)
load_dotenv()

class GeminiWrapper:
    """
    Optional wrapper for Google Gemini API to enhance answer quality.
    This class is safe to import even if the gemini package or API key is missing.
    Actual model calls are only attempted if the package and key are present.
    """

    def __init__(self):
        self.model = None
        self.available = False

        api_key = os.getenv('GEMINI_API_KEY', '').strip()
        if not api_key:
            logger.warning("GEMINI_API_KEY not found or empty. Gemini disabled (but wrapper imported).")
            return

        try:
            # import at runtime so missing package doesn't break imports
            genai = importlib.import_module('google.generativeai')
            genai.configure(api_key=api_key)
            # choose model; keep same name ('gemini-pro')
            self.model = genai.GenerativeModel('gemini-pro')
            self.available = True
            logger.info("✅ Gemini API initialized successfully")
        except ModuleNotFoundError:
            logger.warning("google.generativeai package not installed. Gemini disabled.")
        except Exception as e:
            # catch other errors but do not raise to avoid import-time crashes
            logger.error(f"Failed to initialize Gemini client: {e}")

    def generate_answer(self, question: str, context: str) -> str:
        """
        Generate answer with Gemini if available. Otherwise return a sensible fallback.
        """
        if not self.available or self.model is None:
            # fallback: return context trimmed and a short friendly reply
            trimmed = context.strip()
            if len(trimmed) > 800:
                trimmed = trimmed[:800].rsplit('.', 1)[0] + '.'
            reply = (
                f"{trimmed}\n\n"
                # "Note: Gemini is not configured, so this is the raw extracted NCERT content "
                # "from which you can read the exact explanation. If you want a friendlier summary, "
                # "add a GEMINI_API_KEY to your .env file."
            )
            return reply

        # Build prompt (kept concise & friendly)
        prompt = f"""
You are StudyMate, a warm and patient teacher for school students (Classes 6–10).

Reference NCERT content:
{context[:3000]}

Student question:
{question}

Instructions:
1) Use ONLY the NCERT content above.
2) Answer clearly in 3-6 short sentences. Start with a short definition/explanation then one helpful detail or example.
3) Use simple language appropriate for 10-15 year olds.
4) If not found, reply: "I couldn't find that in the NCERT section I have."
5) Do not say you used the context or mention you are an AI.

Answer:
"""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.35,
                    'top_p': 0.8,
                    'top_k': 40,
                    'max_output_tokens': 300
                }
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}", exc_info=True)
            # safe fallback: trimmed context
            trimmed = context.strip()
            if len(trimmed) > 1000:
                trimmed = trimmed[:1000].rsplit('.', 1)[0] + '.'
            return f"{trimmed}\n\n(Sorry — Gemini call failed; showing extracted content.)"
