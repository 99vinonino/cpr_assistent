import os
import glob
import pandas as pd
from google.cloud import storage
from gcp_app.config import Config

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def read_markdown_files_local(data_dir):
    """Read markdown files from local directory"""
    files = glob.glob(os.path.join(data_dir, "*.md"))
    docs = []
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            docs.append({"filename": os.path.basename(file), "text": f.read()})
    return docs

def read_markdown_files_cloud(bucket_name):
    """Read markdown files from Cloud Storage"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    docs = []
    blobs = bucket.list_blobs()
    
    for blob in blobs:
        if blob.name.endswith('.md'):
            content = blob.download_as_text()
            docs.append({"filename": os.path.basename(blob.name), "text": content})
    
    return docs

def read_markdown_files(data_dir=None, bucket_name=None):
    """Read markdown files from local or cloud storage"""
    if Config.USE_CLOUD_STORAGE and bucket_name:
        return read_markdown_files_cloud(bucket_name)
    else:
        return read_markdown_files_local(data_dir or Config.DATA_DIR)

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def prepare_chunks(data_dir=None, bucket_name=None):
    docs = read_markdown_files(data_dir, bucket_name)
    all_chunks = []
    meta = []
    for doc in docs:
        chunks = chunk_text(doc["text"])
        for idx, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            meta.append({"filename": doc["filename"], "chunk_id": idx, "text": chunk})
    return all_chunks, meta 