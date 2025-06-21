import os
from typing import Optional

class Config:
    # GCP Settings
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "hack-thelaw25cam-577")
    REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    
    # Vertex AI Settings
    EMBEDDING_MODEL = "textembedding-gecko@001"
    LLM_MODEL = "text-bison@001"  # or "gemini-pro"
    
    # Storage Settings
    VECTOR_BUCKET_NAME = os.getenv("VECTOR_BUCKET_NAME", f"{PROJECT_ID}-vectors")
    DATA_BUCKET_NAME = os.getenv("DATA_BUCKET_NAME", f"{PROJECT_ID}-cpr-data")
    VECTOR_FILE = "cpr_embeddings.npy"
    METADATA_FILE = "cpr_metadata.json"
    
    # App Settings
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100
    TOP_K_RESULTS = 5
    
    # Data Settings
    DATA_DIR = "cpr_data" 