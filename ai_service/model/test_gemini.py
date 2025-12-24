import sys
sys.path.insert(0, 'e:\\StudyMate1')

from ai_service.model.gemini_wrapper import GeminiWrapper

# Test the wrapper
wrapper = GeminiWrapper()

print(f"Gemini available: {wrapper.available}")
print(f"Model loaded: {wrapper.model is not None}")

if wrapper.available:
    # Test a simple question
    question = "What is photosynthesis?"
    context = "Photosynthesis is the process by which plants make their own food using sunlight, water, and carbon dioxide."
    
    print("\nTesting answer generation...")
    answer = wrapper.generate_answer(question, context)
    print(f"\nAnswer:\n{answer}")
else:
    print("\n❌ Gemini is not available. Check the logs above for the reason.")
