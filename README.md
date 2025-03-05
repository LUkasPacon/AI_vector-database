# PDFIntelliSearch

An intelligent PDF search engine that implements Retrieval-Augmented Generation (RAG) architecture, combining vector databases (Pinecone) with AI (GPT-4) to provide smart, context-aware answers to your questions about PDF documents.

This tool allows you to upload PDF documents to a Pinecone vector database and perform semantic searches using natural language queries. Using the RAG approach, relevant document chunks are retrieved and used as context for GPT-4 to generate accurate, document-grounded answers.

## Features

- PDF text extraction and intelligent chunking
- Advanced semantic search using OpenAI's text-embedding-3-large model
- Interactive search interface with multiple results
- RAG-based answer generation using GPT-4 with retrieved contexts
- Index management for Pinecone's free tier (5 index limit)
- Support for multiple PDFs in different indexes

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Pinecone API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository
2. Install the required packages:
```bash
python3 -m pip install -r requirements.txt
```
3. Create a `.env` file in the project root with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

## Usage

Run the script:
```bash
python3 pdfintelisearch.py
```

### Main Menu Options

1. **Upload new PDF and create index**
   - Enter path to your PDF file
   - Choose chunk size (default: 800 characters)
   - Set overlap between chunks (default: 200 characters)
   - Name your index (or use default "pdf-search")
   - The script will extract text, create embeddings, and upload to Pinecone
   - After upload, enters search mode automatically

2. **Search in existing index**
   - Choose from list of available indexes
   - Enter search queries in natural language
   - Specify number of results to display (default: 5)
   - Get AI-generated answers based on found contexts

3. **Exit**
   - Quit the program

### Search Tips

- Use specific, focused queries
- Try different formulations of the same question
- Include keywords from the document
- Ask questions naturally - the AI will generate comprehensive answers
- Results show similarity scores (0.3 or higher)
- Each result includes source and relevant text excerpt
- The AI combines all relevant contexts to generate answers

### Index Management

- Maximum 5 indexes in Pinecone's free tier
- Options when limit is reached:
  1. Delete an existing index
  2. Use an existing index
  3. Cancel operation
- Index names can only contain lowercase letters, numbers, and hyphens

## Technical Details

- RAG Architecture:
  - Retrieval: Semantic search in Pinecone vector database
  - Augmentation: Context injection from retrieved chunks
  - Generation: GPT-4 answer synthesis with grounding

- Text Chunking:
  - Default chunk size: 800 characters
  - Default overlap: 200 characters
  - Intelligent paragraph preservation
  - Overlap maintenance for context continuity

- Embeddings:
  - Model: text-embedding-3-large (OpenAI)
  - Batch processing for API efficiency
  - Cosine similarity metric

- Search:
  - Semantic similarity threshold: 0.3
  - Multiple results with scoring
  - Context-aware answer generation
  - GPT-4 for answer synthesis

## Error Handling

- Graceful handling of API errors
- Invalid file path detection
- Index limit management
- Input validation for all user inputs

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

### Apache 2.0 License Summary:
- You can freely use, modify, and distribute this software
- You can use the software for commercial purposes
- You don't have to share the source code of your modifications
- You must retain copyright and license information
- It provides an explicit grant of patent rights from contributors
- It provides no warranty and disclaims liability for damages 

## Ať to fachčí!

## Project Structure

- `pdfintelisearch.py` - Main script implementing the RAG architecture
- `requirements.txt` - List of required Python packages
- `.env` - Configuration file for API keys (not included in repository)
- `INSTRUCTIONS.md` - Detailed usage instructions
- `PDFs/` - Directory for storing PDF documents
- `README.md` - Project documentation and setup guide
