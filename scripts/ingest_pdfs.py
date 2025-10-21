import sys
import os

# Add parent directory to path to import from ai_service
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_service.model.preprocess import PDFPreprocessor
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """
    Ingest and preprocess all NCERT PDFs
    """
    logger.info("="*60)
    logger.info("Starting NCERT PDF Ingestion Process")
    logger.info("="*60)
    
    # Initialize preprocessor
    pdf_dir = os.path.join(os.path.dirname(__file__), '..', 'ai_service', 'data', 'raw_pdfs')
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'ai_service', 'data', 'processed_texts')
    
    preprocessor = PDFPreprocessor(pdf_dir=pdf_dir)
    
    # Process all PDFs
    logger.info(f"PDF Directory: {os.path.abspath(pdf_dir)}")
    logger.info(f"Output Directory: {os.path.abspath(output_dir)}")
    
    processed_data = preprocessor.process_all_pdfs(output_dir=output_dir)
    
    if not processed_data:
        logger.warning("No PDFs were processed!")
        logger.warning(f"Please add NCERT PDF files to: {os.path.abspath(pdf_dir)}")
        return
    
    # Summary
    logger.info("="*60)
    logger.info("Ingestion Complete!")
    logger.info(f"Processed {len(processed_data)} PDF files")
    
    total_chunks = sum(len(chunks) for chunks in processed_data.values())
    logger.info(f"Total text chunks created: {total_chunks}")
    
    logger.info("\nProcessed files:")
    for pdf_name, chunks in processed_data.items():
        logger.info(f"  - {pdf_name}: {len(chunks)} chunks")
    
    logger.info("="*60)
    logger.info("Next step: Run 'python rebuild_embeddings.py' to create vector index")

if __name__ == "__main__":
    main()
