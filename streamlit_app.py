import streamlit as st
import os
from dotenv import load_dotenv
from pdfintelisearch import (
    extract_text_from_pdf,
    chunk_text,
    create_embeddings_and_upload,
    search_in_pdf,
    pc,
    initialize_pinecone
)

# Load environment variables
load_dotenv()

# Initialize Pinecone
initialize_pinecone()

def main():
    st.set_page_config(
        page_title="PDFIntelliSearch",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 PDFIntelliSearch")
    st.markdown("An intelligent PDF search engine with RAG architecture")
    
    # Sidebar for uploading and index management
    with st.sidebar:
        st.header("📑 Document Management")
        
        # File uploader
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        
        # Index management
        st.header("🔍 Index Selection")
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        if existing_indexes:
            selected_index = st.selectbox(
                "Select Index",
                options=existing_indexes,
                help="Choose an existing index to search in"
            )
        else:
            st.info("No indexes available. Please upload a PDF first.")
            selected_index = None
            
        # Advanced settings
        with st.expander("⚙️ Advanced Settings"):
            chunk_size = st.slider("Chunk Size", 300, 2000, 800, 100)
            overlap = st.slider("Overlap Size", 50, 500, 200, 50)
            similarity_threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.3, 0.05)
            max_results = st.slider("Max Results", 1, 10, 5, 1)
    
    # Main area - Upload PDF
    if uploaded_file:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("📄 Upload New PDF")
            
            # Save uploaded file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # Process PDF
            if st.button("Process PDF"):
                with st.spinner("Processing PDF..."):
                    # Extract text
                    text = extract_text_from_pdf(temp_path)
                    if text:
                        st.success(f"Extracted {len(text)} characters")
                        
                        # Create chunks
                        chunks = chunk_text(text, chunk_size, overlap)
                        st.success(f"Created {len(chunks)} chunks")
                        
                        # Create index name from file name
                        index_name = os.path.splitext(uploaded_file.name)[0].lower()
                        index_name = ''.join(c if c.isalnum() else '-' for c in index_name)
                        
                        # Upload to Pinecone
                        success = create_embeddings_and_upload(chunks, uploaded_file.name, index_name)
                        if success:
                            st.success("Successfully uploaded to Pinecone!")
                            selected_index = index_name
                        
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    # Main area - Search
    st.header("🔎 Search")
    
    if selected_index:
        query = st.text_input("Enter your question")
        
        if query:
            with st.spinner("Searching and generating answer..."):
                results = search_in_pdf(
                    query,
                    selected_index,
                    top_k=max_results,
                    similarity_threshold=similarity_threshold,
                    return_results=True
                )
                
                if results and results.get("matches"):
                    # Display results in expandable sections
                    with st.expander("📌 Source Chunks", expanded=True):
                        for i, match in enumerate(results["matches"], 1):
                            st.markdown(f"**Result {i}** (Similarity: {match['score']:.4f})")
                            st.markdown(f"Source: {match['metadata'].get('source', 'Unknown')}")
                            st.text(match['metadata']['text'])
                            st.divider()
                    
                    # Display AI answer
                    st.markdown("### 🤖 AI Answer")
                    answer = results.get("ai_answer", "No answer generated")
                    st.markdown(answer)
                else:
                    st.warning("No results found. Try reformulating your query.")
    else:
        st.info("Please select an index or upload a PDF first.")

if __name__ == "__main__":
    main() 