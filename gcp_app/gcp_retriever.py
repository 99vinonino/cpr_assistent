import numpy as np
import faiss
from typing import List, Dict, Any
from .gcp_embeddings import GCPEmbeddings
from .config import Config

class GCPRetriever:
    def __init__(self):
        self.embeddings_client = GCPEmbeddings()
        self.embeddings = None
        self.metadata = None
        self.index = None
        
    def build_index(self, chunks: List[str], metadata: List[Dict[str, Any]]):
        """Build and save embeddings index"""
        print("Generating embeddings with Vertex AI...")
        embeddings = self.embeddings_client.generate_embeddings(chunks)
        
        print("Saving embeddings to Cloud Storage...")
        self.embeddings_client.save_embeddings(embeddings, metadata)
        
        # Create FAISS index for fast similarity search
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings.astype('float32'))
        
        self.embeddings = embeddings
        self.metadata = metadata
        
    def load_index(self):
        """Load embeddings and metadata from Cloud Storage"""
        print("Loading embeddings from Cloud Storage...")
        self.embeddings, self.metadata = self.embeddings_client.load_embeddings()
        
        # Recreate FAISS index
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings.astype('float32'))
        
    def retrieve(self, query: str, k: int = None) -> List[Dict[str, Any]]:
        """Retrieve top-k most similar chunks"""
        if k is None:
            k = Config.TOP_K_RESULTS
            
        # Generate query embedding
        query_embedding = self.embeddings_client.generate_embeddings([query])
        
        # Search
        D, I = self.index.search(query_embedding.astype('float32'), k)
        
        # Return results
        results = []
        for idx in I[0]:
            results.append(self.metadata[idx])
            
        return results 