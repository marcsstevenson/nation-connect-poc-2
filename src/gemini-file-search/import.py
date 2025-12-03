from google import genai
from google.genai import types
import time
import os

print("GOOGLE_API_KEY:", os.environ['GOOGLE_API_KEY'])

client = genai.Client()

store_name = 'fileSearchStores/lincolnrag-sfqi2owz6ifq'
target_upload_dir = "C:/Temp/lincoln_rag_uploads"

# File name will be visible in citations
# file_search_store = client.file_search_stores.create(config={'display_name': 'lincoln_rag'})
# file_search_store = client.file_search_stores.delete(name='fileSearchStores/lincolnrag-ngzp18t5xhr2')
file_search_store = client.file_search_stores.get(name=store_name)

# TODO: upload all files in target_upload_dir

# TODO: only upload if  the file does not already exist
print(f"Uploading file from {target_upload_dir}/test.txt")
sample_file = client.files.upload(file=f"{target_upload_dir}/test.txt", config={'name': 'testing'})

operation = client.file_search_stores.import_file(
    file_search_store_name=file_search_store.name,
    file_name=sample_file.name
)

while not operation.done:
    time.sleep(5)
    operation = client.operations.get(operation)

for store in client.file_search_stores.list():
    print(store.name, store.display_name, store.active_documents_count)
