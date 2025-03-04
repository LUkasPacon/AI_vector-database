from pinecone import Pinecone, ServerlessSpec
import os
import re
import uuid
from dotenv import load_dotenv
import PyPDF2
from typing import List, Dict, Any
from openai import OpenAI

# Loading environment variables
load_dotenv()

# Initializing Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Initializing OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            print(f"PDF contains {num_pages} pages")
            
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n\n"
                
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Splits text into smaller parts with overlap"""
    chunks = []
    
    # First split text into paragraphs
    paragraphs = re.split(r'\n\s*\n', text)
    
    current_chunk = ""
    for paragraph in paragraphs:
        # If paragraph is too long, split it into smaller parts
        if len(paragraph) > chunk_size:
            words = paragraph.split()
            temp_chunk = ""
            for word in words:
                if len(temp_chunk) + len(word) + 1 <= chunk_size:
                    temp_chunk += word + " "
                else:
                    chunks.append(temp_chunk.strip())
                    # Preserve overlap
                    overlap_words = temp_chunk.split()[-overlap//10:]
                    temp_chunk = " ".join(overlap_words) + " " + word + " "
            if temp_chunk:
                chunks.append(temp_chunk.strip())
        else:
            # If paragraph fits into current chunk, add it
            if len(current_chunk) + len(paragraph) + 2 <= chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                # Otherwise save current chunk and start a new one
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    print(f"Text split into {len(chunks)} parts")
    return chunks

def create_embedding(text: str) -> List[float]:
    """Creates embedding for text using OpenAI API"""
    # Using a more powerful model for embeddings
    response = openai_client.embeddings.create(
        model="text-embedding-3-large",  # Changed to a more powerful model
        input=text,
        encoding_format="float"
    )
    return response.data[0].embedding

def create_embeddings_and_upload(chunks: List[str], pdf_name: str, index_name: str = "pdf-search"):
    """Creates embeddings for chunks and uploads them to Pinecone"""
    try:
        # Creating embeddings
        print(f"Creating embeddings for {len(chunks)} parts...")
        
        # Processing in batches to fit within API limits
        batch_size = 20
        all_vectors = []
        
        # First create one embedding to determine the dimension
        sample_embedding = create_embedding(chunks[0])
        embedding_dimension = len(sample_embedding)
        print(f"Embedding dimension: {embedding_dimension}")
        
        # Add the first embedding to vectors
        all_vectors.append({
            "id": f"pdf_{pdf_name}_0",
            "values": sample_embedding,
            "metadata": {
                "text": chunks[0],
                "source": pdf_name,
                "chunk_index": 0
            }
        })
        
        # Process the rest of the chunks
        for i in range(1, len(chunks), batch_size):
            batch = chunks[i:min(i+batch_size, len(chunks))]
            print(f"Processing batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")
            
            # Creating embeddings using OpenAI
            embeddings = []
            for chunk in batch:
                embedding = create_embedding(chunk)
                embeddings.append(embedding)
            
            # Creating vectors for Pinecone
            for j, (chunk, embedding) in enumerate(zip(batch, embeddings)):
                chunk_id = f"pdf_{pdf_name}_{i+j}"
                all_vectors.append({
                    "id": chunk_id,
                    "values": embedding,
                    "metadata": {
                        "text": chunk,
                        "source": pdf_name,
                        "chunk_index": i+j
                    }
                })
        
        # Connecting to index or creating a new one
        print(f"Checking index: {index_name}")
        
        # Getting list of existing indexes
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        # If index exists, check its dimension
        if index_name in existing_indexes:
            try:
                index_info = pc.describe_index(index_name)
                current_dimension = index_info.dimension
                
                # If dimensions don't match, ask user if they want to delete the index and create a new one
                if current_dimension != embedding_dimension:
                    print(f"WARNING: Existing index has dimension {current_dimension}, but embeddings have dimension {embedding_dimension}.")
                    user_choice = input("Do you want to delete the existing index and create a new one? (yes/no): ")
                    
                    if user_choice.lower() in ["yes", "y"]:
                        print(f"Deleting index {index_name}...")
                        pc.delete_index(index_name)
                        print(f"Creating new index {index_name} with dimension {embedding_dimension}...")
                        # Creating index with us-east-1 region (Virginia), which supports the Starter plan
                        pc.create_index(
                            name=index_name,
                            dimension=embedding_dimension,
                            metric="cosine",
                            spec=ServerlessSpec(cloud="aws", region="us-east-1")
                        )
                    else:
                        print("Operation canceled. Use a different index name or delete the existing index manually.")
                        return False
            except Exception as e:
                print(f"Error checking index: {e}")
                return False
        else:
            # Creating a new index
            print(f"Creating new index {index_name} with dimension {embedding_dimension}...")
            # Creating index with us-east-1 region (Virginia), which supports the Starter plan
            pc.create_index(
                name=index_name,
                dimension=embedding_dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        
        # Wait until the index is ready
        print("Waiting for the index to be ready...")
        import time
        time.sleep(10)  # Wait 10 seconds
        
        # Connect to the index
        index = pc.Index(index_name)
        
        # Upload vectors in batches
        upload_batch_size = 100
        for i in range(0, len(all_vectors), upload_batch_size):
            batch = all_vectors[i:i+upload_batch_size]
            print(f"Uploading batch {i//upload_batch_size + 1}/{(len(all_vectors)-1)//upload_batch_size + 1}")
            index.upsert(vectors=batch)
        
        print(f"Successfully uploaded {len(all_vectors)} vectors to index {index_name}")
        return True
    
    except Exception as e:
        print(f"Error creating embeddings or uploading to Pinecone: {e}")
        import traceback
        traceback.print_exc()
        return False

def search_in_pdf(query: str, index_name: str = "pdf-search", top_k: int = 5):  # Increased default number of results
    """Searches for similar chunks in Pinecone based on query"""
    try:
        # Preprocessing query - removing excess spaces and punctuation
        query = query.strip()
        
        print(f"Searching for: '{query}'")
        
        # Creating embedding for query using OpenAI
        query_embedding = create_embedding(query)
        
        # Connecting to index
        index = pc.Index(index_name)
        
        # Searching for similar vectors
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        if not results["matches"]:
            print("No results found. Try reformulating your query.")
            return None
        
        print(f"\nResults for query: '{query}'")
        
        # Sorting results by similarity score
        sorted_results = sorted(results["matches"], key=lambda x: x["score"], reverse=True)
        
        for i, match in enumerate(sorted_results):
            similarity_score = match["score"]
            # Displaying only results with sufficient similarity
            if similarity_score < 0.5:  # Filtering results with low score
                continue
                
            print(f"\n--- Result {i+1} ---")
            print(f"Similarity score: {similarity_score:.4f}")
            print(f"Source: {match['metadata'].get('source', 'Unknown')}")
            
            # Highlighting relevant parts of text
            text = match['metadata']['text']
            
            # Limiting the length of displayed text, but showing more context
            max_display_length = 800
            if len(text) > max_display_length:
                half_length = max_display_length // 2
                display_text = text[:half_length] + "..." + text[-half_length:]
            else:
                display_text = text
                
            print(f"Text:\n{display_text}")
        
        return results
    
    except Exception as e:
        print(f"Error during search: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    # Path to PDF file
    pdf_path = input("Enter the path to the PDF file: ")
    
    if not os.path.exists(pdf_path):
        print(f"File {pdf_path} does not exist!")
        return
    
    # Extracting text from PDF
    print(f"Extracting text from {pdf_path}...")
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("Failed to extract text from PDF.")
        return
    
    print(f"Extracted {len(text)} characters of text.")
    
    # Splitting text into chunks
    chunk_size = input("Enter chunk size (default: 800): ")  # Smaller default chunk size
    if not chunk_size:
        chunk_size = 800
    else:
        chunk_size = int(chunk_size)
    
    overlap = input("Enter overlap size (default: 200): ")
    if not overlap:
        overlap = 200
    else:
        overlap = int(overlap)
    
    chunks = chunk_text(text, chunk_size, overlap)
    
    # Getting PDF name without path and extension
    pdf_name = os.path.basename(pdf_path)
    pdf_name = os.path.splitext(pdf_name)[0]
    
    # Entering index name
    index_name = input("Enter index name (default: pdf-search): ")
    if not index_name:
        index_name = "pdf-search"
    
    # Validating index name - only lowercase letters, digits, and hyphens
    if not re.match(r'^[a-z0-9\-]+$', index_name):
        print("Index name can only contain lowercase letters, digits, and hyphens.")
        # Automatically fix index name
        index_name = re.sub(r'[^a-z0-9\-]', '-', index_name.lower())
        print(f"Index name has been adjusted to: {index_name}")
    
    # Creating embeddings and uploading to Pinecone
    success = create_embeddings_and_upload(chunks, pdf_name, index_name)
    
    if success:
        print("\nPDF successfully uploaded to Pinecone!")
        
        # Searching
        while True:
            print("\n=== Search in PDF ===")
            print("Tips for better results:")
            print("- Use specific queries")
            print("- Try different formulations of the same query")
            print("- Use keywords from the document")
            
            query = input("\nEnter query (or 'exit' to quit): ")
            
            if query.lower() == "exit":
                break
            
            top_k = input("How many results do you want to display? (default: 5): ")
            if not top_k:
                top_k = 5
            else:
                top_k = int(top_k)
            
            search_in_pdf(query, index_name, top_k=top_k)

if __name__ == "__main__":
    main()