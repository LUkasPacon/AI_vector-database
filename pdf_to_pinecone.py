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

def list_and_manage_indexes():
    """Lists all indexes and allows user to delete them if needed"""
    try:
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        if not existing_indexes:
            print("\nNo existing indexes found.")
            return None
        
        print("\nExisting indexes:")
        for i, index_name in enumerate(existing_indexes, 1):
            print(f"{i}. {index_name}")
        
        if len(existing_indexes) >= 5:  # Starter plan limit
            print("\nWARNING: You've reached the maximum number of indexes (5) for the Starter plan.")
            print("Would you like to:")
            print("1. Delete an existing index")
            print("2. Use an existing index")
            print("3. Cancel operation")
            
            choice = input("\nEnter your choice (1-3): ")
            
            if choice == "1":
                index_num = input("Enter the number of the index to delete: ")
                try:
                    index_num = int(index_num) - 1
                    if 0 <= index_num < len(existing_indexes):
                        index_to_delete = existing_indexes[index_num]
                        pc.delete_index(index_to_delete)
                        print(f"\nIndex '{index_to_delete}' has been deleted.")
                        return None
                    else:
                        print("Invalid index number.")
                        return None
                except ValueError:
                    print("Invalid input.")
                    return None
            elif choice == "2":
                index_num = input("Enter the number of the index to use: ")
                try:
                    index_num = int(index_num) - 1
                    if 0 <= index_num < len(existing_indexes):
                        return existing_indexes[index_num]
                    else:
                        print("Invalid index number.")
                        return None
                except ValueError:
                    print("Invalid input.")
                    return None
            else:
                return None
    except Exception as e:
        print(f"Error managing indexes: {e}")
        return None

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
        
        # Check existing indexes and manage them if needed
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        if index_name in existing_indexes:
            print(f"\nIndex '{index_name}' already exists.")
            user_choice = input("Do you want to (1) overwrite it, (2) use a different name, or (3) cancel? (1/2/3): ")
            
            if user_choice == "1":
                print(f"Deleting existing index '{index_name}'...")
                pc.delete_index(index_name)
            elif user_choice == "2":
                while True:
                    new_name = input("Enter new index name: ")
                    if new_name not in existing_indexes:
                        index_name = new_name
                        break
                    print("That name is also taken. Please try another.")
            else:
                print("Operation cancelled.")
                return False
        elif len(existing_indexes) >= 5:  # Starter plan limit
            print("\nReached maximum number of indexes for Starter plan.")
            managed_index = list_and_manage_indexes()
            if managed_index:
                index_name = managed_index
            else:
                return False
        
        # Create new index if needed
        if index_name not in [index.name for index in pc.list_indexes()]:
            print(f"Creating new index '{index_name}' with dimension {embedding_dimension}...")
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

def generate_answer_with_context(query: str, relevant_chunks: List[Dict], openai_client: OpenAI) -> str:
    """Generates an answer using ChatGPT based on the query and relevant chunks from the document"""
    
    # Prepare context from relevant chunks
    context = "\n\n".join([chunk['metadata']['text'] for chunk in relevant_chunks])
    
    # Create the system message with instructions
    system_message = """You are a helpful assistant that answers questions based on the provided document context. 
    Your answers should be:
    1. Accurate and based only on the provided context
    2. Concise but comprehensive
    3. Include relevant quotes from the context when appropriate
    4. Mention if the context doesn't contain enough information to fully answer the question
    
    Format your response in a clear, readable way."""
    
    # Create the user message with context and query
    user_message = f"""Context from the document:
    ---
    {context}
    ---
    
    Question: {query}
    
    Please provide an answer based on this context."""
    
    try:
        # Call ChatGPT API
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",  # Using the latest GPT-4 model
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error generating answer with ChatGPT: {e}")
        return "Sorry, I couldn't generate an answer at this time."

def search_in_pdf(query: str, index_name: str = "pdf-search", top_k: int = 5):
    """Searches for similar chunks in Pinecone based on query and generates an answer using ChatGPT"""
    try:
        # Preprocessing query - removing excess spaces and punctuation
        query = query.strip()
        
        print(f"Searching for: '{query}'")
        
        # Creating embedding for query using OpenAI
        query_embedding = create_embedding(query)
        
        # Connecting to index
        index = pc.Index(index_name)
        
        # Searching for similar vectors - request more results to account for filtering
        results = index.query(
            vector=query_embedding,
            top_k=top_k * 2,  # Request more results than needed
            include_metadata=True
        )
        
        if not results["matches"]:
            print("No results found. Try reformulating your query.")
            return None
        
        print(f"\nResults for query: '{query}'")
        
        # Sorting results by similarity score
        sorted_results = sorted(results["matches"], key=lambda x: x["score"], reverse=True)
        relevant_chunks = []
        displayed_count = 0
        
        for i, match in enumerate(sorted_results):
            similarity_score = match["score"]
            # Using a lower threshold for similarity
            if similarity_score < 0.3:  # Lowered from 0.5 to 0.3
                continue
                
            print(f"\n--- Result {displayed_count + 1} ---")
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
            relevant_chunks.append(match)
            displayed_count += 1
            
            # Stop after displaying requested number of results
            if displayed_count >= top_k:
                break
        
        print(f"\nFound {displayed_count} relevant results with similarity score above 0.3")
        
        if relevant_chunks:
            print("\nGenerating comprehensive answer based on all found contexts...")
            answer = generate_answer_with_context(query, relevant_chunks, openai_client)
            print("\n=== AI-Generated Answer ===")
            print(answer)
        
        return results
    
    except Exception as e:
        print(f"Error during search: {e}")
        import traceback
        traceback.print_exc()
        return None

def search_mode(index_name: str):
    """Interactive search mode for querying an existing index"""
    while True:
        print("\n=== Search in PDF ===")
        print("Tips for better results:")
        print("- Use specific queries")
        print("- Try different formulations of the same query")
        print("- Use keywords from the document")
        print("- Ask questions naturally - AI will generate comprehensive answers")
        
        query = input("\nEnter query (or 'exit' to quit): ")
        
        if query.lower() == "exit":
            break
        
        top_k = input("How many results do you want to display? (default: 5): ")
        if not top_k:
            top_k = 5
        else:
            top_k = int(top_k)
        
        search_in_pdf(query, index_name, top_k=top_k)

def main():
    print("\n=== PDF to Pinecone Vector Database ===")
    print("1. Upload new PDF and create index")
    print("2. Search in existing index")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        # Path to PDF file
        pdf_path = input("Enter the path to the PDF file: ")
        
        if not os.path.exists(pdf_path):
            print(f"File {pdf_path} does not exist!")
            return
        
        # Show existing indexes before starting
        print("\nChecking existing indexes...")
        list_and_manage_indexes()
        
        # Extracting text from PDF
        print(f"\nExtracting text from {pdf_path}...")
        text = extract_text_from_pdf(pdf_path)
        
        if not text:
            print("Failed to extract text from PDF.")
            return
        
        print(f"Extracted {len(text)} characters of text.")
        
        # Splitting text into chunks
        chunk_size = input("Enter chunk size (default: 800): ")
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
            # Enter search mode
            search_mode(index_name)
            
    elif choice == "2":
        # List available indexes
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        if not existing_indexes:
            print("\nNo existing indexes found. Please upload a PDF first.")
            return
        
        print("\nAvailable indexes:")
        for i, name in enumerate(existing_indexes, 1):
            print(f"{i}. {name}")
        
        while True:
            index_num = input("\nEnter the number of the index to search in: ")
            try:
                index_num = int(index_num) - 1
                if 0 <= index_num < len(existing_indexes):
                    index_name = existing_indexes[index_num]
                    break
                else:
                    print("Invalid index number. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Enter search mode
        search_mode(index_name)
    
    elif choice == "3":
        print("Goodbye!")
        return
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()