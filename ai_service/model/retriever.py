import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
import pickle
import os
import logging

logger = logging.getLogger(__name__)

class DocumentRetriever:
    def __init__(self, index_path: str = None, embedding_model: str = 'all-MiniLM-L6-v2'):
        self.embedding_model = SentenceTransformer(embedding_model)
        self.index = None
        self.documents = []
        
        if index_path:
            self.load_index(index_path)
    
    def load_index(self, base_path: str):
        """Load FAISS index and document metadata"""
        try:
            index_file = os.path.join(base_path, 'faiss_index.bin')
            docs_file = os.path.join(base_path, 'documents.pkl')
            
            if not os.path.exists(index_file) or not os.path.exists(docs_file):
                raise FileNotFoundError(f"Index files not found at {base_path}")
            
            self.index = faiss.read_index(index_file)
            
            with open(docs_file, 'rb') as f:
                data = pickle.load(f)
                
                # Handle both old and new formats
                if isinstance(data, dict):
                    self.documents = data.get('texts', [])
                    self.metadata = data.get('metadata', [])
                else:
                    self.documents = data
                    self.metadata = [{}] * len(data)
            
            logger.info(f"✅ Loaded index with {self.index.ntotal} vectors")
            logger.info(f"✅ Loaded {len(self.documents)} documents")
            
        except Exception as e:
            logger.error(f"❌ Failed to load index: {e}")
            raise
    
    def retrieve_context(self, query: str, top_k: int = 5) -> List[str]:
        """Retrieve most relevant document chunks for a query"""
        if self.index is None or len(self.documents) == 0:
            logger.warning("⚠️ No index loaded!")
            return []
        
        try:
            # Encode query
            query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)
            query_embedding = query_embedding.astype('float32')
            
            # Search
            distances, indices = self.index.search(query_embedding, min(top_k, len(self.documents)))
            
            logger.info(f"🔍 Query: {query[:50]}...")
            logger.info(f"📊 Retrieved {len(indices[0])} documents")
            logger.info(f"📏 Distances: {distances[0][:3]}")
            
            # Get documents
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx < len(self.documents):
                    doc = self.documents[idx]
                    
                    # Extract text
                    if isinstance(doc, dict):
                        text = doc.get('text', '') or doc.get('content', '') or str(doc)
                    elif isinstance(doc, str):
                        text = doc
                    else:
                        text = str(doc)
                    
                    if text and len(text.strip()) > 50:
                        results.append(text)
                        
                        # Log with metadata if available
                        source = self.metadata[idx].get('source', 'unknown') if idx < len(self.metadata) else 'unknown'
                        logger.debug(f"  - Doc {idx} from {source}: {text[:100]}... (distance: {distance:.4f})")
            
            logger.info(f"✅ Successfully extracted {len(results)} text chunks")
            if results:
                logger.info(f"📄 First result (300 chars): {results[0][:300]}...")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Retrieval error: {e}", exc_info=True)
            return []
