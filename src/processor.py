import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()
def process_pdf(file_path):
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Using OpenRouter for Embeddings
    embeddings = OpenAIEmbeddings(
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        model="openai/text-embedding-3-small", # Standard embedding model
        check_embedding_ctx_length=False       # Required for OpenRouter
    )
    
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    
    vectorstore = FAISS.from_documents(
        documents=splits, 
        embedding=embeddings
    )
    return vectorstore.as_retriever()