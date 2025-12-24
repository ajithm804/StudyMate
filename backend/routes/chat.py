from flask import Blueprint, request, jsonify
import logging
import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ai_service.model.qa_system import QASystem

logger = logging.getLogger(__name__)

# Initialize QA system (do this once when app starts)
INDEX_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'ai_service', 'data', 'index')
qa_system = QASystem(index_path=INDEX_PATH, use_gemini=True)

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        logger.info(f"📥 Received question: {question}")
        
        # Get answer using QA system (retrieval + Gemini)
        result = qa_system.answer_question(question, top_k=5)
        
        response = {
            'answer': result['answer'],
            'sources': result['sources'],
            'enhanced_by_ai': result['used_gemini']
        }
        
        logger.info(f"📤 Sending response (Gemini: {result['used_gemini']})")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"❌ Chat error: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
