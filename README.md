# PDF to Pinecone Vector Database

This project enables text extraction from PDF documents, splitting it into smaller chunks, creating vector representations using OpenAI embeddings, and storing them in a Pinecone vector database for efficient semantic searching.

## Features

- **PDF Text Extraction** - Automatic loading and extraction of text from PDF documents
- **Intelligent Chunking** - Splitting text into smaller parts with adjustable size and overlap
- **Vectorization with OpenAI** - Creation of high-quality embeddings using the `text-embedding-3-large` model
- **Pinecone Storage** - Efficient storage of vectors in the Pinecone database
- **Semantic Search** - Finding relevant information using natural language
- **Interactive Interface** - Simple user interface for uploading and searching

## Requirements

- Python 3.7+
- OpenAI API key
- Pinecone API key
- Dependencies installed from `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <directory-name>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your-openai-api-key
   PINECONE_API_KEY=your-pinecone-api-key
   ```

## Usage

Run the script with the command:
```bash
python3 pdf_to_pinecone.py
```

### Uploading a PDF to Pinecone

1. Select the option to upload a PDF to Pinecone
2. Enter the path to the PDF file
3. Optionally set the chunk size and overlap
4. Wait for the process to complete

### Searching in the Document

1. Select the option to search in the document
2. Enter your query in natural language
3. View the results sorted by relevance

## How It Works

### 1. PDF Text Extraction
The script uses the PyPDF2 library to extract text from all pages of the PDF document.

### 2. Text Chunking
The extracted text is divided into smaller overlapping parts (chunks) for efficient processing and searching.

### 3. Creating Embeddings
For each chunk, an embedding (vector representation) is created using the OpenAI API and the `text-embedding-3-large` model.

### 4. Storing in Pinecone
Embeddings are stored in the Pinecone vector database along with metadata containing the original text and information about the position in the document.

### 5. Searching
When searching, the query is converted to an embedding and compared with the stored vectors in Pinecone. Results are sorted by similarity.

## Optimization

- **Chunk Size**: Smaller chunks (500-1000 characters) are suitable for precise searching of specific information, larger chunks (1500-2000 characters) preserve more context.
- **Overlap**: Larger overlap (200-300 characters) ensures that information at chunk boundaries is not lost.
- **Embeddings Model**: The `text-embedding-3-large` model provides high-quality vector representations for accurate searching.

## Project Structure

- `pdf_to_pinecone.py` - Main script
- `requirements.txt` - List of dependencies
- `.env` - File with API keys (not included in the repository)
- `PDF_INSTRUCTIONS.md` - Detailed usage instructions
- `PDFs/` - Directory for storing PDF files

## License

This project is licensed under the Apache License 2.0 - see the [official license text](https://www.apache.org/licenses/LICENSE-2.0).

### Apache 2.0 License Summary:
- You can freely use, modify, and distribute this software
- You can use the software for commercial purposes
- You don't have to share the source code of your modifications
- You must retain copyright and license information
- It provides an explicit grant of patent rights from contributors
- It provides no warranty and disclaims liability for damages 

## Ať to fachčí!
