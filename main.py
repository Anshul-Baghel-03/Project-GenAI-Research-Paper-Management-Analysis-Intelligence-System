"""
Script : Embeddings & Vector Store
===============================================
This script demonstrates creating embeddings and building a vector store.

Run with: python main.py
"""

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from core.document_processor import DocumentProcessor
from core.embeddings import EmbeddingManager
from core.vector_store import VectorStoreManager
from config.settings import Settings
import pprint

def main():
    print("\n" + "=" * 70)
    print("🎓 Creating Embeddings & Vector Store")
    print("=" * 70)
    
    # Step 1: Loading and Processing documents
    print("\n📄 Step 1: Loading and Processing documents...")
    processor = DocumentProcessor(chunk_size=150, chunk_overlap=30)
    chunks, section, metadata = processor.process("data\documents\sample file.pdf")
    print(f"✅ Split into {len(chunks)} chunks")
    pprint.pprint(metadata, indent= 4)
    
    print("\n" + "="*70)
    print(f"Research Paper Sections: \n")
    
    pprint.pprint(section, indent=4)
    
    print("\n" + "="*70)
    
    # Step 2: Create embeddings
    print("\n🔢 Step 2: Creating embeddings...")
    print("   (Downloading model on first run - this may take a minute...)")
    embedder = EmbeddingManager(model_name="sentence-transformers/all-MiniLM-L6-v2")
    print("✅ Embedding model loaded")
    print(f"   Model: {embedder.model_name}")
    print(f"   Dimension: {embedder.get_embedding_dimension()}")
    
    # Step 3: Build vector store
    print("\n📊 Step 3: Building vector store...")
    vs_manager = VectorStoreManager(embedder)
    vs_manager.create_from_documents(chunks)
    print(f"✅ Vector store created with {len(chunks)} documents")
    
    # Step 4: Test semantic search
    print("\n🔍 Step 4: Testing semantic search...")
    test_queries = [
        "what is about this pdf?",
        "summarise the document?",
        "Tell me what is Three-Level Hierarchical Evaluation Framework",
        "how the Population-Level Performance Assessment is done?"
    ]
    
    for query in test_queries:
        print(f"\n   Query: '{query}'")
        results = vs_manager.search(query, k=2)
        for i, doc in enumerate(results, 1):
            print(f"   {i}. {doc.page_content[:150]}...")
    
    # Step 5: Save vector store
    print("\n💾 Step 5: Saving vector store...")
    vs_manager.save(path=Settings.FAISS_INDEX_PATH)
    print(f"✅ Vector store saved to {vs_manager.index_path}/")
    
    # Step 6: Load and verify
    print("\n📂 Step 6: Loading saved vector store...")
    vs_loader = VectorStoreManager(embedder)
    vs_loader.load(path=Settings.FAISS_INDEX_PATH)
    print("✅ Vector store loaded successfully")
    
    # Verify it works
    test_result = vs_loader.search("Scoring Methodology", k=1)
    print(f"✅ Verification search returned: {test_result[0].page_content[:150]}...")
    
    # Statistics
    print("\n" + "=" * 70)
    print("📊 STATISTICS")
    print("=" * 70)
    print(f"Documents indexed: {len(chunks)}")
    print(f"Embedding dimension: {embedder.get_embedding_dimension()}")
    print(f"Vector store location: {vs_manager.index_path}")
    
   


if __name__ == "__main__":
    main()