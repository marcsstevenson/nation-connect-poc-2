# Gemini File Search RAG System

A Python-based RAG (Retrieval-Augmented Generation) system using Google's Gemini File Search API with for document question-answering.

## Features

- **File Search Store Management**: Create and manage Gemini file search stores
- **Document Import**: Batch upload documents from local directories
- **RAG Search**: Query documents using natural language with Gemini's file search
- **Evaluation System**: Automated testing and scoring of RAG responses
- **Store Cleanup**: Utilities to delete files and stores

Note also that images within documents are being included in the embedding database.

## Installation

1. **Clone or navigate to this directory**

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   Create a `.env` file in the root directory based on `example.env`:

   ```
   GOOGLE_API_KEY=your_api_key_here
   STORE_NAME=fileSearchStores/your-store-name
   TARGET_UPLOAD_DIR=path/to/your/documents
   ```

## Scripts

### Core Scripts

#### `create.py`

Creates a new file search store in Google Gemini. Lists all existing stores with their document counts.

```bash
python create.py
```

#### `import.py`

Imports files from a local directory into a Gemini file search store. Handles file sanitization, duplicate detection, and batch upload with progress tracking.

```bash
python import.py
```

#### `search.py`

Interactive search script to query documents in the file search store. Uses Gemini file search RAG to answer questions based on uploaded documents.

```bash
python search.py
```

### Evaluation

#### `evals.py`

Evaluation script for testing file search RAG system performance. Reads questions from `evals.csv`, generates answers, scores them with LLM, and exports results to `eval-results.csv`.

```bash
python evals.py
```

Expected CSV format for `evals.csv`:

```
question,expected_answer
"What is X?","X is..."
"When did Y happen?","Y happened in..."
```

### Cleanup Scripts

#### `delete-search-store.py`

Deletes all documents from a specific file search store. Removes both the document references and the underlying files.

```bash
python delete-search-store.py
```

#### `delete-all-files.py`

**Warning**: Permanently deletes all files from the Gemini client across all stores.

```bash
python delete-all-files.py
```

## Usage Workflow

1. **Create a store**: Run `create.py` to create a new file search store
2. **Import documents**: Configure `TARGET_UPLOAD_DIR` in `.env` and run `import.py`
3. **Search documents**: Modify questions in `search.py` and run to query your documents
4. **Evaluate performance**: Create `evals.csv` with test questions and run `evals.py`

## File Search Store

The system uses Gemini's file search stores to enable RAG capabilities:

- Documents are uploaded and indexed for semantic search
- File names appear in citations when answering questions
- Supports various document formats (PDF, TXT, DOCX, etc.)
- Automatic duplicate detection prevents re-uploading existing files
