# backend/rag/ingest.py
import os
import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Paths: this script is at backend/rag/ingest.py, so project root is three levels up
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PDF_FOLDER = os.path.join(BASE_DIR, "knowledge")
PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")

if not os.path.exists(PDF_FOLDER):
    raise FileNotFoundError(f"PDF folder not found: {PDF_FOLDER}")
os.makedirs(PERSIST_DIR, exist_ok=True)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

documents = []
pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]

if not pdf_files:
    logger.warning("No PDF files found.")
else:
    for filename in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, filename)
        try:
            logger.info(f"Loading: {filename}")
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
        except Exception as e:
            logger.error(f"Failed to load {filename}: {e}")

logger.info(f"Pages loaded: {len(documents)}")
if not documents:
    raise RuntimeError("No documents loaded – cannot create vector store.")

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(documents)
logger.info(f"Chunks: {len(docs)}")

try:
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
except Exception as e:
    raise RuntimeError(f"Failed to load embedding model: {e}")

vectordb = Chroma.from_documents(documents=docs, embedding=embedding_model, persist_directory=PERSIST_DIR)
if hasattr(vectordb, "persist"):
    vectordb.persist()

logger.info(f"Vector store created at {PERSIST_DIR}, chunks: {len(docs)}")