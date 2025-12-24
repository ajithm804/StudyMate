# ai_service/gemini_wrapper.py
import os
import sys
import logging
from typing import Optional
from dotenv import load_dotenv
import importlib
from pathlib import Path

# Fix for packages installed in wrong venv location
sys.path.insert(0, r'E:\StudyMate\.venv\Lib\site-packages')

logger = logging.getLogger(__name__)

# Try multiple locations for .env file
env_paths = [
    Path(__file__).parent.parent / '.env',  # ai_service/.env
    Path(__file__).parent.parent.parent / '.env',  # project root/.env
]

for env_path in env_paths:
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        logger.info(f"Loaded .env from: {env_path}")
        break
else:
    logger.warning("No .env file found in expected locations")

class GeminiWrapper:
    """
    Optional wrapper for Google Gemini API to enhance answer quality.
    This class is safe to import even if the gemini package or API key is missing.
    Actual model calls are only attempted if the package and key are present.
    """

    def __init__(self):
        self.client = None
        self.available = False

        # Check if Gemini is enabled
        use_gemini = os.getenv('USE_GEMINI', 'false').lower() == 'true'
        if not use_gemini:
            logger.info("USE_GEMINI is disabled. Gemini wrapper will not initialize.")
            return

        api_key = os.getenv('GEMINI_API_KEY', '').strip()
        if not api_key:
            logger.warning("GEMINI_API_KEY not found or empty. Gemini disabled (but wrapper imported).")
            return

        try:
            # import new google.genai package - correct syntax
            import google.genai as genai
            self.client = genai.Client(api_key=api_key)
            self.available = True
            logger.info("✅ Gemini API initialized successfully with google.genai")
        except (ModuleNotFoundError, ImportError) as e:
            logger.warning(f"google.genai package not installed. Install with: pip install google-genai. Error: {e}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}", exc_info=True)

    def generate_answer(self, question: str, context: str) -> str:
        """
        Generate answer with Gemini if available. Otherwise return a sensible fallback.
        """
        if not self.available or self.client is None:
            # fallback: return context trimmed and a short friendly reply
            trimmed = context.strip()
            if len(trimmed) > 800:
                trimmed = trimmed[:800].rsplit('.', 1)[0] + '.'
            return trimmed

        # Build prompt for detailed, educational answers
        prompt = f"""You are a helpful NCERT tutor for Class 6-10 students.

Reference material:
{context[:3000]}

Student question: {question}

Instructions: Write a detailed, complete explanation (at least 5-6 sentences) using the reference material. Explain clearly with examples. Use simple language suitable for school students.

Your detailed answer:"""

        try:
            response = self.client.models.generate_content(
                model='models/gemini-2.5-flash',
                contents=prompt,
                config={
                    'temperature': 0.7,
                    'top_p': 0.95,
                    'max_output_tokens': 1024,  # Increased to allow complete answers
                }
            )
            
            # Get the full text from response
            answer = ""
            
            if hasattr(response, 'text') and response.text:
                answer = response.text.strip()
            elif hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        answer = ''.join(part.text for part in candidate.content.parts if hasattr(part, 'text'))
            
            return answer if answer else context[:800]
            
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}", exc_info=True)
            # safe fallback: trimmed context
            trimmed = context.strip()
            if len(trimmed) > 1000:
                trimmed = trimmed[:1000].rsplit('.', 1)[0] + '.'
            return f"{trimmed}\n\n(Sorry — Gemini call failed; showing extracted content.)"
