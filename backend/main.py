# backend/main.py

from fastapi import FastAPI
from backend.schemas import PatientInput
from backend.model_service import predict_diabetes
from backend.report_service import generate_gpt_report
from backend.graph_builder import graph

app = FastAPI(
    title="SmartGraphDx API",
    version="1.0"
)


@app.get("/")
def root():
    return {
        "message": "SmartGraphDx MaaS API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/predict")
def predict(patient: PatientInput):
    return predict_diabetes(patient)


@app.post("/explain")
def explain(patient: PatientInput):

    prediction = predict_diabetes(patient)

    result = graph.invoke({
        "probability": prediction["probability"],
        "risk_level": prediction["risk_level"],
        "risk_factors": prediction["risk_factors"],
        "evidence": "",
        "explanation": "",
        "risk_advice": "",
        "lifestyle_advice": "",
        "monitoring_advice": "",
        "summary": ""
    })

    return result


@app.post("/report")
def report(patient: PatientInput):

    prediction = predict_diabetes(patient)

    result = graph.invoke({
        "probability": prediction["probability"],
        "risk_level": prediction["risk_level"],
        "risk_factors": prediction["risk_factors"],
        "evidence": "",
        "explanation": "",
        "risk_advice": "",
        "lifestyle_advice": "",
        "monitoring_advice": "",
        "summary": ""
    })

    report_text = generate_gpt_report(
        prediction=prediction["prediction"],
        probability=prediction["probability"],
        risk_level=prediction["risk_level"],
        risk_factors=prediction["risk_factors"],
        evidence=result["evidence"]
    )

    return {
        "report": report_text
    }