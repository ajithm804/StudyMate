import logging
from typing import Dict, List
from .retriever import DocumentRetriever
from .gemini_wrapper import GeminiWrapper

logger = logging.getLogger(__name__)

class QASystem:
    """
    Question-Answering system that combines document retrieval with Gemini AI enhancement.
    """
    
    def __init__(self, index_path: str = None, use_gemini: bool = True):
        """
        Initialize QA system with retriever and optional Gemini wrapper.
        
        Args:
            index_path: Path to FAISS index directory
            use_gemini: Whether to use Gemini for answer enhancement (default: True)
        """
        self.retriever = DocumentRetriever(index_path=index_path)
        self.gemini = GeminiWrapper() if use_gemini else None
        
        logger.info(f"QA System initialized")
        logger.info(f"  - Retriever: {'✅ Loaded' if self.retriever.index else '❌ Not loaded'}")
        logger.info(f"  - Gemini: {'✅ Available' if self.gemini and self.gemini.available else '❌ Disabled'}")
    
    def answer_question(self, question: str, top_k: int = 5) -> Dict:
        """
        Answer a question using retrieval + Gemini enhancement.
        
        Args:
            question: Student's question
            top_k: Number of documents to retrieve
            
        Returns:
            Dict with 'answer', 'context', 'sources', 'used_gemini'
        """
        try:
            # Step 1: Retrieve relevant context from NCERT documents
            logger.info(f"📚 Retrieving context for: {question[:100]}...")
            retrieved_docs = self.retriever.retrieve_context(question, top_k=top_k)
            
            if not retrieved_docs:
                logger.warning("⚠️ No relevant documents found")
                return {
                    'answer': "I couldn't find relevant information in the NCERT material for your question. Could you try rephrasing it?",
                    'context': [],
                    'sources': [],
                    'used_gemini': False
                }
            
            # Step 2: Combine retrieved documents into context
            combined_context = '\n\n'.join(retrieved_docs[:3])  # Use top 3 for context
            logger.info(f"📄 Combined context length: {len(combined_context)} characters")
            
            # Step 3: Generate answer using Gemini (if available) or return context
            if self.gemini and self.gemini.available:
                logger.info("🤖 Generating answer with Gemini...")
                answer = self.gemini.generate_answer(question, combined_context)
                used_gemini = True
            else:
                logger.info("📝 Using direct context (Gemini not available)")
                # Fallback: return a formatted version of the context
                answer = self._format_context_as_answer(combined_context)
                used_gemini = False
            
            logger.info(f"✅ Answer generated ({len(answer)} chars)")
            
            return {
                'answer': answer,
                'context': retrieved_docs[:3],
                'sources': self._extract_sources(retrieved_docs),
                'used_gemini': used_gemini
            }
            
        except Exception as e:
            logger.error(f"❌ Error answering question: {e}", exc_info=True)
            return {
                'answer': "Sorry, I encountered an error while processing your question. Please try again.",
                'context': [],
                'sources': [],
                'used_gemini': False
            }
    
    def _format_context_as_answer(self, context: str, max_length: int = 800) -> str:
        """Format retrieved context as a readable answer (fallback when Gemini unavailable)"""
        trimmed = context.strip()
        if len(trimmed) > max_length:
            trimmed = trimmed[:max_length].rsplit('.', 1)[0] + '.'
        return trimmed
    
    def _extract_sources(self, documents: List[str]) -> List[str]:
        """Extract source information from retrieved documents"""
        sources = []
        for i, doc in enumerate(documents[:3], 1):
            if i < len(self.retriever.metadata):
                source = self.retriever.metadata[i].get('source', f'NCERT Document {i}')
                sources.append(source)
            else:
                sources.append(f'NCERT Document {i}')
        return sources
