
"""
Chat Interface Module
=====================
DAY 4: Main chat interface logic.

SOLID Principle: Single Responsibility Principle (SRP)
- This module handles chat orchestration

Topics to teach:
- Streamlit chat elements
- Streaming responses
- Error handling
- User experience
"""

import streamlit as st
from typing import Generator, Optional

from core.document_processor import DocumentProcessor
from core.vector_store import VectorStoreManager
from core.chain import RAGChain
from ui.components import add_message, save_uploaded_file
from langchain_core.documents import Document



class ChatInterface:
    """
    Main chat interface orchestrator.
    
    Coordinates between:
    - Document processing
    - Vector store
    - RAG chain
    """
    
    def __init__(self):
        """Initialize chat interface components."""
        self.doc_processor = DocumentProcessor()
        self.vector_store = VectorStoreManager()
        self.rag_chain: Optional[RAGChain] = None
    
    def process_uploaded_files(self, uploaded_files) -> int:
        """
        Process uploaded files and add to vector store.
        
        Args:
            uploaded_files: List of Streamlit UploadedFile objects
            
        Returns:
            Number of chunks processed
        """
        all_chunks = []
        
        for uploaded_file in uploaded_files:
            # Save file temporarily
            file_path = save_uploaded_file(uploaded_file)
            
            # Process the document
            chunks = self.doc_processor.process(file_path)
            
            # Add source metadata
            flat_chunks = []
            for chunk in chunks:
                if isinstance(chunk, list):
                    flat_chunks.extend(chunk)
                else:
                    flat_chunks.append(chunk)
            
            cleaned_chunks = []
            for item in flat_chunks:
                if isinstance(item, Document):
                    item.metadata["source"] = uploaded_file.name
                    cleaned_chunks.append(item)

                elif isinstance(item, dict):
                    # Convert dict → Document
                    doc = Document(
                        page_content=item.get("page_content", ""),
                        metadata=item.get("metadata", {})
                    )
                    doc.metadata["source"] = uploaded_file.name
                    cleaned_chunks.append(doc)

                else:
                    # Skip unknown types safely
                    continue

            all_chunks.extend(cleaned_chunks)
            
            # Track uploaded files
            if uploaded_file.name not in st.session_state.uploaded_files:
                st.session_state.uploaded_files.append(uploaded_file.name)
        
        # Add to vector store
        if all_chunks:
            self.vector_store.add_documents(all_chunks)
            st.session_state.vector_store_initialized = True
        
        return len(all_chunks)
    
    def initialize_rag_chain(self):
        """Initialize the RAG chain after documents are loaded."""
        if self.vector_store.is_initialized:
            self.rag_chain = RAGChain(self.vector_store)

    
    def get_response(
        self,
        query: str
    ) -> Generator[str, None, None]:
        """
        Get a streaming response for a query.
        
        Args:
            query: User's question
            
        Yields:
            Response chunks
        """
        # Initialize RAG chain if needed
        if self.rag_chain is None:
            self.initialize_rag_chain()
        
        # If no documents , provide helpful message
        if not self.vector_store.is_initialized:
            yield "Please upload some documents first to get started!"
            return
        
        
        doc_results = []
        if self.vector_store.is_initialized:
                doc_results = self.vector_store.search(query)
                

            # Format context
        context_parts = []
            
        if doc_results:
                context_parts.append("=== From Your Documents ===")
                for i, doc in enumerate(doc_results, 1):
                    source = doc.metadata.get("source", "Unknown")
                    context_parts.append(f"[Doc {i}] ({source}):\n{doc.page_content}")
                    print(f"vectore-store_result:{doc.page_content}")
            
            
        context = "\n\n".join(context_parts) if context_parts else "No context available."

        # Generate response with context
        from langchain_groq import ChatGroq
        from langchain_core.prompts import ChatPromptTemplate
        from config.settings import settings
            
        llm = ChatGroq(
                model=settings.LLM_MODEL,
                temperature=settings.LLM_TEMPERATURE,
                api_key=settings.GROQ_API_KEY
            )
            
        prompt = ChatPromptTemplate.from_template(
                "Based on the following search results, answer the question concisely and accurately.\n\n"
                "Search Results:\n{context}\n\n"
                "Question: {question}\n\n"
                "Answer: "
            )
            
        chain = prompt | llm
        for chunk in chain.stream({"context": context, "question": query}):
            yield chunk.content
        
    
    def get_sources(self, query: str) -> list:
        """
        Get source documents for a query.
        
        Args:
            query: User's question
            
        Returns:
            List of source document names
        """
        sources = []
        
        # Get semantic search sources
        if self.vector_store.is_initialized:
            docs = self.vector_store.search(query)
            sources.extend(list(set(doc.metadata.get("source", "Unknown") for doc in docs)))
        
        return sources
