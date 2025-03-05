# Instructions for Uploading PDF to Pinecone

I have created a script `pdf_to_pinecone.py` that allows you to extract text from a PDF file, split it into smaller parts, create embeddings using the `text-embedding-3-large` model, and upload them to a Pinecone database. You can then search the PDF content using semantic queries.

## What the Script Does

1. Extracts text from a PDF file
2. Splits the text into smaller parts (chunks) with adjustable size and overlap
3. Creates embeddings for each chunk using the `text-embedding-3-large` model
4. Uploads vectors to a Pinecone index
5. Allows searching in the PDF content using semantic queries

## Installing Dependencies

Before running the script, you need to install the necessary dependencies:

```bash
python3 -m pip install pinecone-client>=3.0.0 python-dotenv PyPDF2>=3.0.0 openai>=1.0.0
```

## How to Use the Script

1. Open a terminal
2. Navigate to the project directory:
   ```
   cd /path/to/your/project
   ```

3. Run the script:
   ```
   python3 pdf_to_pinecone.py
   ```

4. Follow the interactive prompts:
   - Enter the path to the PDF file
   - Optionally set the chunk size and overlap
   - After uploading the data, you can start searching the PDF content

## Usage Example

```
Enter the path to the PDF file: /path/to/your/document.pdf
Enter chunk size (default: 1000): 800
Enter overlap size (default: 200): 100

...

=== Search in PDF ===
Enter query (or 'exit' to quit): What are the main advantages of artificial intelligence?
How many results do you want to display? (default: 5): 2

...

=== Search in PDF ===
Enter query (or 'exit' to quit): exit
```

## Tips for Optimal Use

1. **Chunk Size**: 
   - Smaller chunks (500-800 characters) are suitable for precise searching of specific information
   - Larger chunks (1000-2000 characters) preserve more context but may be less precise

2. **Overlap Size**:
   - Larger overlap (200-300 characters) helps capture information that might otherwise be split between chunks
   - Smaller overlap saves space in the database

3. **Query Formulation**:
   - Use natural questions or phrases
   - Experiment with different formulations for better results
   - Include specific keywords from the document when possible

## Troubleshooting

- **Error extracting text from PDF**: Some PDF files may be protected or use non-standard formatting. Try another PDF file or use a tool for preliminary conversion of PDF to text.

- **Error creating embeddings**: Make sure you have correctly set up the OpenAI API key and that you have sufficient credits.

- **Memory issues**: If you're processing very large PDF files, you may run out of memory. Try reducing the chunk size or processing the PDF in parts.

## Extending Functionality

You can further extend the script to include:

1. Support for more document formats (DOCX, TXT, HTML)
2. Extraction of metadata from PDFs (author, creation date, keywords)
3. Filtering results by metadata
4. Visualization of search results
5. Hybrid search combining vector and keyword search 