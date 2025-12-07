"""
Utility script to delete all files from the Gemini Files.
Warning: This will permanently delete all files across all Gemini File stores.
"""

from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini API client
client = genai.Client()

print("Deleting all files from client.files")

# Iterate through all files and delete them
deleted_count = 0
for file in client.files.list():
    print(f"Deleting {file.display_name} ({file.name})")
    client.files.delete(name=file.name)
    deleted_count += 1

print(f"Successfully deleted {deleted_count} files")

