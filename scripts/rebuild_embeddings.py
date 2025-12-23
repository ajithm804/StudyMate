import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_service.model.embeddings import EmbeddingManager
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """
    Rebuild FAISS embeddings from processed texts
    """
    logger.info("="*60)
    logger.info("Starting Embedding Rebuild Process")
    logger.info("="*60)
    
    processed_dir = os.path.join(
        os.path.dirname(__file__), 
        '..', 
        'ai_service', 
        'data', 
        'processed_texts'
    )
    
    # Check if processed texts exist
    if not os.path.exists(processed_dir):
        logger.error(f"Processed texts directory not found: {processed_dir}")
        logger.error("Please run 'python ingest_pdfs.py' first!")
        return
    
    text_files = [f for f in os.listdir(processed_dir) if f.endswith('.txt')]
    if not text_files:
        logger.error(f"No processed text files found in: {processed_dir}")
        logger.error("Please run 'python ingest_pdfs.py' first!")
        return
    
    logger.info(f"Found {len(text_files)} processed text files")
    
    # Initialize embedding manager
    manager = EmbeddingManager()
    
    # Build embeddings and index
    logger.info("Building embeddings and FAISS index...")
    index, texts, metadata = manager.build_from_processed_texts(processed_dir=processed_dir)
    
    # Save the index
    logger.info("Saving FAISS index and metadata...")
    manager.save_index(index, texts, metadata)
    
    logger.info("="*60)
    logger.info("Embedding Rebuild Complete!")
    logger.info(f"Total vectors in index: {index.ntotal}")
    logger.info(f"Vector dimension: {manager.dimension}")
    logger.info("="*60)
    logger.info("✅ AI Service is ready! You can now start the application.")

if __name__ == "__main__":
    main()
