"""
Script to delete all documents from a specific file search store.
Removes both the document references and the underlying files.
"""

from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

store_name = os.getenv('STORE_NAME')

# Initialize the Gemini API client
client = genai.Client()

# Retrieve the file search store by name
file_search_store = client.file_search_stores.get(name=store_name)

print(f"Deleting all files from store: {store_name}")

# Iterate through all documents in the store and delete them
deleted_count = 0
for doc in client.file_search_stores.documents.list(parent=store_name):
    print(f"Deleting {doc.display_name} ({doc.name})")
    # Delete the document from the file search store
    client.file_search_stores.documents.delete(name=doc.name, config={'force': True})
    # Delete the underlying file from storage
    client.files.delete(name=doc.name, config={'force': True})

    deleted_count += 1

print(f"Successfully deleted {deleted_count} files from store")
