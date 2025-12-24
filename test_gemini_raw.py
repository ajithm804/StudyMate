import sys
sys.path.insert(0, r'E:\StudyMate\.venv\Lib\site-packages')

import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('e:/StudyMate1/ai_service/.env')
load_dotenv(dotenv_path=env_path)

import google.genai as genai

api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

prompt = """Answer this question in detail (minimum 5 sentences):

What is photosynthesis?

Be thorough and complete your answer."""

print("Testing raw API call...\n")

response = client.models.generate_content(
    model='models/gemini-2.5-flash',
    contents=prompt,
    config={
        'temperature': 0.7,
        'max_output_tokens': 1000,
    }
)

print("RESPONSE:")
print("="*60)
print(response.text)
print("="*60)
print(f"\nLength: {len(response.text)} characters")
print(f"Candidates: {len(response.candidates) if hasattr(response, 'candidates') else 'N/A'}")

if hasattr(response, 'candidates') and response.candidates:
    print(f"Finish reason: {response.candidates[0].finish_reason if hasattr(response.candidates[0], 'finish_reason') else 'N/A'}")
