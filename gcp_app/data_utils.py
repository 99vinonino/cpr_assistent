import os
import glob
import pandas as pd

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def read_markdown_files(data_dir):
    files = glob.glob(os.path.join(data_dir, "*.md"))
    docs = []
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            docs.append({"filename": os.path.basename(file), "text": f.read()})
    return docs

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def prepare_chunks(data_dir):
    docs = read_markdown_files(data_dir)
    all_chunks = []
    meta = []
    for doc in docs:
        chunks = chunk_text(doc["text"])
        for idx, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            meta.append({"filename": doc["filename"], "chunk_id": idx, "text": chunk})
    return all_chunks, meta 