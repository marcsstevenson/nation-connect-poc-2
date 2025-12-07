"""
Script to import files from a local directory into a Gemini file search store.
Handles file sanitization, duplicate detection, and batch upload with progress tracking.
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
target_upload_dir = os.getenv('TARGET_UPLOAD_DIR')

def sanitize_resource_name(filename):
    """
    Convert filename to valid resource name format:
    - Only lowercase alphanumeric characters or dashes
    - Cannot begin or end with a dash
    - Maximum 40 characters
    """
    # Convert to lowercase
    name = filename.lower()
    # Replace invalid characters with dashes
    name = re.sub(r'[^a-z0-9-]', '-', name)
    # Remove leading/trailing dashes
    name = name.strip('-')
    # Replace multiple consecutive dashes with single dash
    name = re.sub(r'-+', '-', name)
    # Truncate to 40 characters
    if len(name) > 40:
        name = name[:40]
    # Remove trailing dash if truncation created one
    name = name.rstrip('-')
    return name

# Initialize the Gemini API client
client = genai.Client()

# Retrieve the existing file search store
file_search_store = client.file_search_stores.get(name=store_name)

# Get list of existing files to avoid duplicate uploads
existing_files = set()
for doc in client.file_search_stores.documents.list(parent=store_name):
    existing_files.add(doc.display_name)

print(f"Found {len(existing_files)} existing files in store")

# Process each file in the target upload directory
for filename in os.listdir(target_upload_dir):
    file_path = os.path.join(target_upload_dir, filename)

    # Only process files, not directories
    if os.path.isfile(file_path):
        resource_name = sanitize_resource_name(filename)

        # Skip if file already exists in store (avoid duplicates)
        if resource_name in existing_files:
            print(f"Skipping {filename} - already exists in store")
            continue

        print(f"Uploading file from {file_path} with name {resource_name}")

        # Detect MIME type for proper file handling
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        # Upload file to Gemini with binary mode for proper encoding
        with open(file_path, 'rb') as f:
            uploaded_file = client.files.upload(
                file=f,
                config={
                    'name': resource_name,
                    'display_name': filename,
                    'mime_type': mime_type
                }
            )

        # Import the uploaded file into the search store
        operation = client.file_search_stores.import_file(
            file_search_store_name=file_search_store.name,
            file_name=uploaded_file.name
        )

        # Wait for the import operation to complete
        while not operation.done:
            time.sleep(5)
            operation = client.operations.get(operation)

        print(f"Successfully uploaded and imported {filename}")

# Display final status of all file search stores
for store in client.file_search_stores.list():
    print(store.name, store.display_name, store.active_documents_count)
