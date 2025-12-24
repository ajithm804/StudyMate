import logging
import sys

# Add the correct site-packages to path
sys.path.insert(0, r'E:\StudyMate1\.venv\Lib\site-packages')

# Set up logging to see error messages
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

sys.path.insert(0, 'e:\\StudyMate1')

from ai_service.model.gemini_wrapper import GeminiWrapper

# Test the wrapper
wrapper = GeminiWrapper()

print(f"\nGemini available: {wrapper.available}")
print(f"Client loaded: {wrapper.client is not None}")

if wrapper.available:
    # Test a simple question
    question = "What is photosynthesis?"
    context = "Photosynthesis is the process by which plants make their own food using sunlight, water, and carbon dioxide. The green pigment chlorophyll in leaves absorbs sunlight. This energy is used to convert carbon dioxide from air and water from soil into glucose (sugar) and oxygen. The glucose provides energy for the plant's growth and development. The oxygen is released into the air as a byproduct."
    
    print("\nTesting answer generation...")
    answer = wrapper.generate_answer(question, context)
    
    print(f"\n{'='*60}")
    print("FULL ANSWER:")
    print(f"{'='*60}")
    print(answer)
    print(f"{'='*60}")
    print(f"\nAnswer length: {len(answer)} characters")
    print(f"Sentence count: ~{answer.count('.')}")
    print(f"{'='*60}")
else:
    print("\n❌ Gemini is not available. Check the logs above for the reason.")
