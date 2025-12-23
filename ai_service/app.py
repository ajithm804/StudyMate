from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="StudyMate AI Service", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

class HealthResponse(BaseModel):
    status: str
    message: str

@app.get("/", response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    return {
        "status": "success",
        "message": "StudyMate AI Service is running"
    }

# Initialize response engine
VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'vector_store')

try:
    if not os.path.exists(os.path.join(VECTOR_STORE_PATH, 'faiss_index.bin')):
        logger.warning("⚠️ Vector store not found! Run: python scripts/rebuild_embeddings.py")
        response_engine = None
    else:
        from model.response_engine import ResponseEngine
        
        # Check if Gemini key exists
        gemini_key = os.getenv('GEMINI_API_KEY')
        has_gemini = bool(gemini_key and len(gemini_key.strip()) > 10)
        
        logger.info(f"🔑 Gemini API Key configured: {has_gemini}")
        
        response_engine = ResponseEngine(
            vector_store_path=VECTOR_STORE_PATH,
            use_gemini=True  # Always try to use Gemini if available
        )
        logger.info("✅ Response engine initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize: {e}", exc_info=True)
    response_engine = None

@app.post("/ask")
async def ask_question(request: Query):
    if response_engine is None:
        raise HTTPException(
            status_code=503,
            detail="AI service is not ready. Please ensure PDFs are ingested and embeddings are built."
        )
    
    try:
        question = request.question
        logger.info(f"📨 Question received: {question}")
        
        # Get answer
        answer = response_engine.get_answer(question)
        
        logger.info(f"✅ Answer sent")
        
        return {
            "answer": answer,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    # Check if vector store exists
    vector_store_path = "data/vector_store/faiss_index.faiss"
    if not os.path.exists(vector_store_path):
        logger.warning(
            "Vector store not found! Please run scripts/ingest_pdfs.py "
            "and scripts/rebuild_embeddings.py first."
        )
    
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
