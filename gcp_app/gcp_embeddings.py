import numpy as np
import json
from google.cloud import aiplatform
from google.cloud import storage
from typing import List, Dict, Any
from .config import Config

class GCPEmbeddings:
    def __init__(self):
        aiplatform.init(project=Config.PROJECT_ID, location=Config.REGION)
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(Config.BUCKET_NAME)
        
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings using Vertex AI"""
        embeddings = []
        # Vertex AI supports batching up to 5 texts at a time for gecko
        batch_size = 5
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = aiplatform.TextEmbeddingModel.from_pretrained(
                Config.EMBEDDING_MODEL
            ).get_embeddings(batch)
            
            for embedding in response:
                embeddings.append(embedding.values)
                
        return np.array(embeddings)
    
    def save_embeddings(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]]):
        """Save embeddings and metadata to Cloud Storage"""
        # Save embeddings
        blob = self.bucket.blob(Config.VECTOR_FILE)
        blob.upload_from_string(embeddings.tobytes())
        
        # Save metadata
        metadata_blob = self.bucket.blob(Config.METADATA_FILE)
        metadata_blob.upload_from_string(json.dumps(metadata))
        
    def load_embeddings(self) -> tuple:
        """Load embeddings and metadata from Cloud Storage"""
        # Load embeddings
        blob = self.bucket.blob(Config.VECTOR_FILE)
        embeddings_bytes = blob.download_as_bytes()
        embeddings = np.frombuffer(embeddings_bytes).reshape(-1, 768)  # Adjust dimension as needed
        
        # Load metadata
        metadata_blob = self.bucket.blob(Config.METADATA_FILE)
        metadata = json.loads(metadata_blob.download_as_text())
        
        return embeddings, metadata 