"""
Script to create a new file search store in Google Gemini.
Creates a new store and lists all existing stores with their document counts.
"""

from google import genai
from google.genai import types
import time
import os
import re
import mimetypes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

store_name = os.getenv('STORE_NAME')

# Initialize the Gemini API client
client = genai.Client()

# Delete an existing store (cleanup from previous runs)
client.file_search_stores.delete(name='fileSearchStores/lincolnrag-sfqi2owz6ifq')

# Create a new file search store with display name
# File names will be visible in citations when answering questions
file_search_store = client.file_search_stores.create(config={'display_name': 'lincoln_rag'})

# List all file search stores with their metadata
for store in client.file_search_stores.list():
    print(store.name, store.display_name, store.active_documents_count)
