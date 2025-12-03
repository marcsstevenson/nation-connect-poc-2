from google import genai
from google.genai import types
import time
import os

print("GOOGLE_API_KEY:", os.environ['GOOGLE_API_KEY'])

client = genai.Client()

store_name = 'fileSearchStores/lincolnrag-sfqi2owz6ifq'

# File name will be visible in citations
# sample_file = client.files.upload(file="C:/Temp/test.txt", config={'name': 'testing'})

# file_search_store = client.file_search_stores.get(config={'display_name': 'lincoln_rag'})
# file_search_store = client.file_search_stores.delete(name='fileSearchStores/lincolnrag-ngzp18t5xhr2')
# file_search_store = client.file_search_stores.get(name=store_name)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="""What is the name of the testing document?""",
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[store_name]
                )
            )
        ]
    )
)

print(response.text)


