import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader
import os
import uuid

# Initialize ChromaDB with persistent storage
chroma_client = chromadb.PersistentClient(path="knowledge_base_db")

# Create collection with embedding function
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection = chroma_client.get_or_create_collection(
    name="personal_knowledge", 
    embedding_function=sentence_transformer_ef
)

def extract_text_from_pdf(file_path: str) -> str:
    """Extract and clean text from PDF"""
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = "\n".join([
            page.extract_text() or ""  # Handle None returns
            for page in reader.pages
        ])
    return text.strip()

def add_documents_to_knowledge(folder_path: str, chunk_size: int = 1000):
    """Process PDFs with proper chunking and unique IDs"""
    documents = []
    metadatas = []
    ids = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}...")
            
            try:
                content = extract_text_from_pdf(file_path)
                if not content:
                    print(f"Skipping {filename} - no text extracted")
                    continue
                
                # Split content into chunks
                words = content.split()
                for i in range(0, len(words), chunk_size):
                    chunk = ' '.join(words[i:i+chunk_size])
                    documents.append(chunk)
                    metadatas.append({
                        "source": filename,
                        "type": "pdf",
                        "pages": len(PdfReader(file_path).pages),
                        "chunk": f"{i//chunk_size + 1}"
                    })
                    ids.append(str(uuid.uuid4()))  # Generate unique ID
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue
    
    if documents:
        collection.upsert(  # Using upsert instead of add to prevent duplicates
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(documents)} document chunks to knowledge base")

def query_knowledge(question: str, n_results: int = 3):
    """Improved query with better error handling"""
    try:
        results = collection.query(
            query_texts=[question],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        if not results['documents'][0]:
            print("No results found")
            return
        
        print(f"\nTop {min(n_results, len(results['documents'][0]))} results for: '{question}'\n")
        for i, (doc, meta, dist) in enumerate(zip(results['documents'][0], 
                                               results['metadatas'][0], 
                                               results['distances'][0])):
            print(f"################################### {i} ###################################")
            print(f"Result {i+1} (Relevance: {1-dist:.2f})")
            print(f"Source: {meta['source']} (Chunk {meta['chunk']} of {meta['pages']} pages)")
            print("Content preview:\n", doc[:200].replace("\n", " ") + "...\n")
    
    except Exception as e:
        print(f"Query failed: {str(e)}")

# Example usage
if __name__ == "__main__":
    pdf_folder = "./knowledge_base_db"  # Update this path
    add_documents_to_knowledge(pdf_folder)
    
    while True:
        question = input("\nTalk with your PDFs?")
        if question.lower() == 'quit':
            break
        query_knowledge(question)

# How to use:
# Put your PDFs file into the "knowledge_base_db" folder.
# Then run and ask with your program about your PDFs.
