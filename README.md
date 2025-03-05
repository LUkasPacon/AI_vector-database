# PDFIntelliSearch

An intelligent PDF search engine that implements Retrieval-Augmented Generation (RAG) architecture, combining vector databases (Pinecone) with AI (GPT-4) to provide smart, context-aware answers to your questions about PDF documents.

## Features

- PDF text extraction and intelligent chunking
- Advanced semantic search using OpenAI's text-embedding-3-large model
- Interactive search interface with multiple results
- RAG-based answer generation using GPT-4 with retrieved contexts
- Index management for Pinecone's free tier (5 index limit)
- Support for multiple PDFs in different indexes
- Modern Streamlit GUI for easy interaction

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Pinecone API key (free tier supported)
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

You can run PDFIntelliSearch in two modes:

### 1. Command Line Interface
```bash
python3 pdfintelisearch.py
```

### 2. Graphical User Interface (Recommended)
```bash
streamlit run streamlit_app.py
```

The GUI provides a user-friendly interface with:
- Drag & drop PDF upload
- Interactive index selection
- Real-time search results
- Advanced settings controls
- Beautiful visualization of results

## Features in Detail

### PDF Processing
- Automatic text extraction
- Smart chunking with configurable size and overlap
- Preservation of document structure
- Support for multiple PDF documents

### Vector Search
- OpenAI's text-embedding-3-large model for high-quality embeddings
- Pinecone vector database for efficient similarity search
- Configurable similarity threshold (default: 0.3)
- Multiple results with relevance scores

### RAG Implementation
1. **Retrieval**:
   - Semantic search in Pinecone vector database
   - Smart filtering of results based on similarity
   - Support for multiple relevant chunks

2. **Augmentation**:
   - Context preparation from retrieved chunks
   - Intelligent chunk selection
   - Metadata preservation

3. **Generation**:
   - GPT-4 Turbo for answer synthesis
   - Context-aware responses
   - Source attribution
   - Confidence indicators

### GUI Features
- **Document Management**:
  - PDF file upload via drag & drop
  - Index selection dropdown
  - Document source tracking

- **Search Interface**:
  - Natural language query input
  - Real-time search results
  - Expandable result sections
  - AI-generated answers

- **Advanced Settings**:
  - Chunk size adjustment (300-2000 characters)
  - Overlap size control (50-500 characters)
  - Similarity threshold tuning (0.0-1.0)
  - Number of results selection (1-10)

## Technical Details

### Vector Database
- **Pinecone Configuration**:
  - Serverless deployment on AWS
  - Cosine similarity metric
  - 3072-dimensional vectors
  - Batch processing for efficiency

### Embeddings
- Model: text-embedding-3-large
- Dimension: 3072
- Batch processing
- Error handling and retry logic

### Search Algorithm
- Two-phase similarity search
- Dynamic threshold adjustment
- Result ranking and filtering
- Metadata enrichment

## Error Handling

- Graceful handling of API errors
- Invalid file path detection
- Index limit management
- Input validation
- Automatic cleanup of temporary files

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Project Structure

- `pdfintelisearch.py` - Core RAG implementation
- `streamlit_app.py` - GUI implementation
- `requirements.txt` - Dependencies
- `.env` - Configuration (not in repo)
- `README.md` - Documentation
- `PDFs/` - Optional directory for PDF storage

## Tips for Best Results

1. **Document Preparation**:
   - Use clear, well-formatted PDFs
   - Ensure good text extraction quality
   - Consider document length and structure

2. **Search Optimization**:
   - Use specific, focused queries
   - Experiment with chunk sizes for your use case
   - Adjust similarity threshold based on needs

3. **Performance**:
   - Monitor API usage
   - Use batch processing for large documents
   - Clean up unused indexes

## Troubleshooting

Common issues and solutions:
1. API key errors: Check .env file
2. Index limit: Manage or delete unused indexes
3. PDF extraction: Verify PDF format and accessibility
4. Search quality: Adjust chunk size and overlap
5. GUI issues: Check Streamlit installation

## Future Improvements

Planned features:
1. Hybrid search (semantic + keyword)
2. Multi-document querying
3. Custom embedding models
4. Export and sharing capabilities
5. Advanced visualization options
