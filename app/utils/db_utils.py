import os
import chromadb
from chromadb.config import Settings

def get_db_client():
    """Initialize and return a ChromaDB client."""
    persist_directory = os.getenv('CHROMA_DB_PATH', './data/processed/chroma_db')
    client = chromadb.PersistentClient(path=persist_directory)
    return client

def get_or_create_collection(client, collection_name):
    """Get an existing collection or create a new one if it doesn't exist."""
    return client.get_or_create_collection(collection_name)

def add_documents(collection, documents, metadatas, ids):
    """Add documents to the specified collection."""
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

def query_collection(collection, query_text, n_results=5):
    """Query the collection and return results."""
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results