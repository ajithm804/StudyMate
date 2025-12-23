from .retriever import DocumentRetriever
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

class ResponseEngine:
    def __init__(self, vector_store_path: str, use_gemini: bool = True):  # Changed default to True
        self.retriever = DocumentRetriever(index_path=vector_store_path)
        self.use_gemini = False
        self.gemini = None
        
        # Try to initialize Gemini if requested
        if use_gemini:
            try:
                from .gemini_wrapper import GeminiWrapper
                gemini_key = os.getenv('GEMINI_API_KEY')
                if gemini_key and len(gemini_key.strip()) > 10:
                    self.gemini = GeminiWrapper()
                    self.use_gemini = True
                    logger.info("✅ Using Gemini for enhanced responses")
                else:
                    logger.warning("⚠️ GEMINI_API_KEY not found in .env file")
                    logger.info("ℹ️ Falling back to smart extraction")
            except ImportError:
                logger.warning("⚠️ google-generativeai not installed")
                logger.info("💡 Install with: pip install google-generativeai")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Gemini: {e}")
                logger.info("ℹ️ Falling back to smart extraction")
        
        if not self.use_gemini:
            logger.info("📝 Using smart extraction (no Gemini)")
    
    def get_answer(self, question: str) -> str:
        """Get answer for a question"""
        try:
            logger.info(f"📨 Question: {question}")
            logger.info(f"🤖 Using Gemini: {self.use_gemini}")
            
            # Retrieve relevant context
            contexts = self.retriever.retrieve_context(question, top_k=5)
            
            if not contexts:
                logger.warning("⚠️ No relevant context found")
                return "I apologize, but I couldn't find relevant information in the NCERT materials to answer your question. Please try rephrasing or asking about topics covered in NCERT textbooks for classes 6-10 (Science, Maths, or English)."
            
            logger.info(f"✅ Found {len(contexts)} relevant contexts")
            
            # Combine contexts
            combined_context = "\n\n".join(contexts[:3])
            logger.info(f"📝 Context length: {len(combined_context)} chars")
            
            # Generate response
            if self.use_gemini and self.gemini:
                logger.info("🤖 Generating answer with Gemini...")
                answer = self.gemini.generate_answer(question, combined_context)
            else:
                logger.info("📝 Extracting answer without Gemini...")
                answer = self._extract_smart_answer(question, contexts)
            
            logger.info(f"✅ Generated answer: {answer[:100]}...")
            return answer
            
        except Exception as e:
            logger.error(f"❌ Error generating answer: {e}", exc_info=True)
            return f"I encountered an error while processing your question: {str(e)}"
    
    def _extract_smart_answer(self, question: str, contexts: list) -> str:
        """Smart answer extraction without AI"""
        question_lower = question.lower()
        
        # Get the most relevant context
        best_context = contexts[0] if contexts else ""
        
        # Split into sentences
        sentences = [s.strip() + '.' for s in best_context.split('.') if len(s.strip()) > 20]
        
        # Identify question type and extract accordingly
        if 'what did' in question_lower or 'what does' in question_lower:
            # Extract action sentences
            name_words = [w for w in question.split() if w[0].isupper() and len(w) > 2]
            action_sentences = []
            
            for sent in sentences:
                if any(name in sent for name in name_words):
                    if any(verb in sent.lower() for verb in ['asked', 'told', 'gave', 'made', 'went', 'took', 'planted', 'did', 'followed']):
                        action_sentences.append(sent)
            
            if action_sentences:
                return ' '.join(action_sentences[:3])
        
        elif 'who is' in question_lower or 'who was' in question_lower:
            # Return first 2-3 sentences
            return ' '.join(sentences[:3])
        
        elif 'why' in question_lower:
            # Look for reason sentences
            reason_sentences = [s for s in sentences if any(word in s.lower() for word in ['because', 'so that', 'to ', 'in order'])]
            if reason_sentences:
                return ' '.join(reason_sentences[:2])
        
        elif 'how' in question_lower:
            # Return process sentences
            return ' '.join(sentences[:4])
        
        # Default: return first few sentences
        return ' '.join(sentences[:3])
