# backend/rag/retriever.py
import os
import logging
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3

retriever = None
try:
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embedding)
    retriever = vectordb.as_retriever(search_kwargs={"k": TOP_K})
    logger.info("ChromaDB loaded")
except Exception as e:
    logger.warning(f"ChromaDB not available: {e}")

def get_fallback_evidence(risk_factors):
    """Generate relevant guidelines based on risk factors."""
    evidence_pieces = []
    if "High BMI" in risk_factors:
        evidence_pieces.append("• Obesity: Weight loss of 5-10% reduces diabetes risk by 58% (Diabetes Prevention Program).")
    if "Elevated HbA1c" in risk_factors or "Elevated Blood Glucose" in risk_factors:
        evidence_pieces.append("• Prediabetes: Lifestyle intervention reduces progression to diabetes by 71% in adults over 60 (ADA).")
    if "Hypertension" in risk_factors:
        evidence_pieces.append("• Hypertension: Target BP <130/80 mmHg for diabetics (ADA Standards of Care 2024).")
    if "Current Smoker" in risk_factors:
        evidence_pieces.append("• Smoking cessation: Reduces cardiovascular risk and improves glycemic control (WHO).")
    if not evidence_pieces:
        evidence_pieces.append("• Regular physical activity (150 min/week) and healthy diet are primary prevention (ADA).")
    return "\n".join(evidence_pieces)

def retrieve_evidence(query: str) -> str:
    # Extract risk factors from query (simple heuristic)
    risk_factors = []
    if "High BMI" in query: risk_factors.append("High BMI")
    if "Elevated HbA1c" in query: risk_factors.append("Elevated HbA1c")
    if "Hypertension" in query: risk_factors.append("Hypertension")
    if "Smoker" in query: risk_factors.append("Current Smoker")
    
    if retriever:
        try:
            docs = retriever.invoke(query)
            if docs:
                return "\n\n".join(doc.page_content for doc in docs)
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
    return get_fallback_evidence(risk_factors)