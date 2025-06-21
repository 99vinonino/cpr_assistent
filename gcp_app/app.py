import streamlit as st
import json
from typing import List, Dict, Any
from .data_utils import prepare_chunks
from .gcp_retriever import GCPRetriever
from .gcp_llm import GCPLLM
from .config import Config

# Page config
st.set_page_config(
    page_title="CPR Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

# Initialize session state
if 'retriever' not in st.session_state:
    st.session_state.retriever = None
if 'llm' not in st.session_state:
    st.session_state.llm = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def initialize_services():
    """Initialize GCP services"""
    if st.session_state.retriever is None:
        with st.spinner("Initializing GCP services..."):
            st.session_state.retriever = GCPRetriever()
            st.session_state.llm = GCPLLM()
            
            # Try to load existing index, otherwise build new one
            try:
                st.session_state.retriever.load_index()
                st.success("Loaded existing knowledge base!")
            except:
                st.info("Building new knowledge base...")
                chunks, metadata = prepare_chunks(Config.DATA_DIR)
                st.session_state.retriever.build_index(chunks, metadata)
                st.success("Knowledge base built successfully!")

def main():
    st.title("⚖️ CPR Legal Assistant")
    st.markdown("Your AI-powered guide through Civil Procedure Rules and Practice Directions")
    
    # Sidebar for user type and settings
    with st.sidebar:
        st.header("Settings")
        user_type = st.selectbox(
            "I am a:",
            ["Private Individual", "Legal Professional"],
            help="This helps tailor the response to your expertise level"
        )
        
        st.markdown("---")
        st.markdown("**Powered by:**")
        st.markdown("- Vertex AI Embeddings")
        st.markdown("- Vertex AI PaLM/Gemini")
        st.markdown("- Cloud Storage")
        
    # Initialize services
    initialize_services()
    
    # Main chat interface
    st.header("Ask a Legal Question")
    
    # Chat input
    query = st.text_input(
        "Ask about civil procedure, forms, or legal processes:",
        placeholder="e.g., How do I serve a claim form? What track will my case be allocated to?"
    )
    
    if query:
        # Add to chat history
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        # Retrieve relevant documents
        with st.spinner("Searching knowledge base..."):
            retrieved = st.session_state.retriever.retrieve(query)
            context = "\n\n".join([f"Source: {r['filename']}\n{r['text']}" for r in retrieved])
        
        # Generate answer
        with st.spinner("Generating answer..."):
            answer = st.session_state.llm.generate_answer(context, query)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
        
        # Display answer
        st.markdown("### Answer")
        st.write(answer)
        
        # Generate checklist if requested
        if "checklist" in query.lower() or "steps" in query.lower():
            with st.spinner("Generating checklist..."):
                checklist = st.session_state.llm.generate_checklist(context, query)
                
                st.markdown("### Step-by-Step Checklist")
                for item in checklist:
                    st.markdown(f"**{item['step']}.** {item['description']}")
        
        # Display sources
        with st.expander("📚 Sources"):
            for r in retrieved:
                st.markdown(f"- **{r['filename']}** (chunk {r['chunk_id']})")
                st.markdown(f"  > {r['text'][:200]}...")
        
        # Export options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Export to Notion", help="Export checklist to Notion (coming soon)"):
                st.info("Notion integration coming soon!")
        
        with col2:
            if st.button("📄 Download as PDF", help="Download answer as PDF"):
                st.info("PDF export coming soon!")
    
    # Chat history
    if st.session_state.chat_history:
        st.markdown("---")
        st.header("Chat History")
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Assistant:** {message['content']}")
        
        if st.button("Clear History"):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    main() 