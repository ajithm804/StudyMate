import os
import pickle
import logging
from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import re

logger = logging.getLogger(__name__)

class EmbeddingManager:
    """
    Manages creation and storage of text embeddings using SentenceTransformers and FAISS
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding model
        
        Args:
            model_name: Name of the SentenceTransformer model
        """
        self.model_name = model_name
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"Embedding dimension: {self.dimension}")
        
        # Vector store path
        self.vector_store_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'data', 
            'vector_store'
        )
        os.makedirs(self.vector_store_path, exist_ok=True)
        
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Create embeddings for a list of text chunks
        
        Args:
            texts: List of text strings
            
        Returns:
            Numpy array of embeddings
        """
        logger.info(f"Creating embeddings for {len(texts)} text chunks")
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        return embeddings
    
    def build_faiss_index(self, embeddings: np.ndarray) -> faiss.Index:
        """
        Build FAISS index for fast similarity search
        
        Args:
            embeddings: Numpy array of embeddings
            
        Returns:
            FAISS index
        """
        logger.info("Building FAISS index")
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Create index
        index = faiss.IndexFlatIP(self.dimension)  # Inner Product (cosine similarity)
        index.add(embeddings)
        
        logger.info(f"FAISS index built with {index.ntotal} vectors")
        return index
    
    def build_index(self, texts: list):
        """Build FAISS index from text chunks"""
        logger.info(f"Building FAISS index for {len(texts)} chunks...")
        
        # Generate embeddings
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        embeddings = embeddings.astype('float32')
        
        logger.info(f"Generated embeddings shape: {embeddings.shape}")
        
        # Create FAISS index
        index = faiss.IndexFlatL2(self.dimension)
        index.add(embeddings)
        
        logger.info(f"✅ Index built with {index.ntotal} vectors")
        
        return index
    
    def build_from_processed_texts(self, processed_dir: str):
        """Build index from processed text files"""
        logger.info(f"Loading texts from: {processed_dir}")
        
        texts = []
        metadata = []  # Store source information
        
        # Walk through all subdirectories
        for root, dirs, files in os.walk(processed_dir):
            for file in files:
                if file.endswith('.txt'):
                    filepath = os.path.join(root, file)
                    logger.info(f"Reading: {filepath}")
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Split by chunk markers
                        chunks = re.split(r'={3,}\s*CHUNK\s+\d+\s*={3,}', content)
                        chunks = [c.strip() for c in chunks if len(c.strip()) > 100]
                        
                        if not chunks:
                            # Fallback: split normally if no markers
                            chunks = self._split_text(content, chunk_size=1000, overlap=200)
                        
                        # Add source information to each chunk
                        source = os.path.splitext(file)[0]
                        for chunk in chunks:
                            texts.append(chunk)
                            metadata.append({'source': source, 'file': file})
                        
                        logger.info(f"  ✓ Extracted {len(chunks)} chunks")
                        
                    except Exception as e:
                        logger.error(f"  ✗ Error reading {file}: {e}")
        
        if not texts:
            raise ValueError("No text chunks found!")
        
        logger.info(f"Total chunks: {len(texts)}")
        logger.info(f"Sample chunk (first 300 chars):\n{texts[0][:300]}...")
        
        # Build index
        index = self.build_index(texts)
        
        return index, texts, metadata
    
    def _split_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> list:
        """Split text into overlapping chunks by sentences"""
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            if current_length + sentence_length > chunk_size and current_chunk:
                # Save current chunk
                chunks.append(' '.join(current_chunk))
                
                # Keep last few sentences for overlap
                overlap_sentences = []
                overlap_length = 0
                for s in reversed(current_chunk):
                    if overlap_length + len(s) <= overlap:
                        overlap_sentences.insert(0, s)
                        overlap_length += len(s)
                    else:
                        break
                
                current_chunk = overlap_sentences
                current_length = overlap_length
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        # Add last chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return [c for c in chunks if len(c.strip()) > 50]
    
    def save_index(self, index, texts: list, metadata: list = None):
        """Save FAISS index and document texts with metadata"""
        # Save FAISS index
        index_file = os.path.join(self.vector_store_path, 'faiss_index.bin')
        faiss.write_index(index, index_file)
        logger.info(f"✅ Saved index to: {index_file}")
        
        # Save texts with metadata
        docs_file = os.path.join(self.vector_store_path, 'documents.pkl')
        data_to_save = {
            'texts': texts,
            'metadata': metadata or [{}] * len(texts)
        }
        with open(docs_file, 'wb') as f:
            pickle.dump(data_to_save, f)
        logger.info(f"✅ Saved {len(texts)} documents with metadata")
        
        # Save embeddings for reference
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        embeddings_file = os.path.join(self.vector_store_path, 'embeddings.npy')
        np.save(embeddings_file, embeddings)
        logger.info(f"✅ Saved embeddings to: {embeddings_file}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    manager = EmbeddingManager()
    index, texts, metadata = manager.build_from_processed_texts()
    manager.save_index(index, texts, metadata)
    
    print(f"Successfully built and saved index with {len(texts)} chunks")
