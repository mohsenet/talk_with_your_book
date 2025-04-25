# PDF Knowledge Base with ChromaDB RAG System

This repository contains a Python implementation of a Retrieval-Augmented Generation (RAG) system using ChromaDB as the vector database. The system allows you to index PDF documents, create embeddings, and query your personal knowledge base using natural language.

## Features

- 📄 Extract text from PDF documents
- 🔢 Generate embeddings using Sentence Transformers
- 💾 Store embeddings persistently with ChromaDB
- 🔍 Query your knowledge base with natural language
- 📊 Get relevance scores for search results

## Prerequisites

- Python 3.7+
- pip package manager

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/mohsenet/talk_with_your_book.git
   cd talk_with_your_book
   ```

2. Install the required dependencies:
   ```bash
   pip install chromadb sentence-transformers pypdf
   ```

3. Create a directory for your knowledge base:
   ```bash
   mkdir knowledge_base_db
   ```

## Usage

### Adding Documents to Your Knowledge Base

1. Place your PDF files in the `knowledge_base_db` folder.

2. Run the script to process and index your documents:
   ```bash
   python main.py
   ```

3. The script will automatically:
   - Extract text from each PDF
   - Split the text into manageable chunks
   - Generate embeddings for each chunk
   - Store the embeddings in the ChromaDB database

### Querying Your Knowledge Base

After indexing your documents, you can query your knowledge base using natural language:

1. When prompted, enter your question or query.
2. The system will return the most relevant passages from your documents, ranked by relevance.
3. Type 'quit' to exit the application.

## How It Works

### Text Extraction and Chunking

The system extracts text from PDF files and splits it into chunks of a configurable size (default: 1000 words). Each chunk is processed independently to:
- Maintain context within reasonable segments
- Allow for more precise retrieval
- Optimize embedding quality

### Embedding Generation

The system uses the `all-MiniLM-L6-v2` model from Sentence Transformers to generate embeddings. This model:
- Creates 384-dimensional embeddings
- Balances quality and performance
- Works well for general knowledge retrieval

### Vector Storage and Retrieval

ChromaDB is used as the vector database to:
- Store document embeddings persistently
- Perform efficient similarity searches
- Return ranked results based on semantic similarity

## Why ChromaDB for RAG?

ChromaDB offers several advantages for implementing Retrieval-Augmented Generation systems:

1. **Open-source and lightweight**: Easily integrates into any project without heavy infrastructure requirements.

2. **Simple API**: Provides intuitive methods for adding, querying, and managing vector embeddings.

3. **Persistence**: Offers both in-memory and disk-based storage options.

4. **Collection-based organization**: Helps organize embeddings by topic or source.

5. **Metadata support**: Allows storing and querying additional information alongside embeddings.

6. **Efficient similarity search**: Optimized for fast retrieval of semantically similar content.

7. **Local deployment**: Can be run entirely locally, ensuring data privacy and reducing latency.

8. **Active development**: Regularly updated with new features and optimizations.

## Customizing the System

### Changing the Embedding Model

To use a different embedding model, modify the following line:

```python
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"  # Change to your preferred model
)
```

### Adjusting Chunk Size

To change how documents are split, modify the chunk_size parameter:

```python
add_documents_to_knowledge(pdf_folder, chunk_size=500)  # Smaller chunks
```

### Modifying Result Count

To change the number of results returned for each query:

```python
query_knowledge(question, n_results=5)  # Return 5 results
```

## Limitations

- Currently only supports PDF files
- Basic text extraction without special handling for tables or images
- Limited to the capabilities of the chosen embedding model

## Future Improvements

- Support for additional document formats (DOCX, TXT, etc.)
- Improved text extraction with OCR capabilities
- Web interface for easier interaction
- Integration with language models for enhanced response generation

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
