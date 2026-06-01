# frontend/streamlit_app.py

import streamlit as st
import requests

# =====================================================
# CONFIGURATION
# =====================================================

API_URL = "http://localhost:8000"
# For Render deployment:
# API_URL = "https://your-fastapi-service.onrender.com"

st.set_page_config(
    page_title="SmartGraphDx",
    layout="wide"
)

st.title("🩺 SmartGraphDx")
st.subheader("Personalized Graph-Based Diabetes Risk Assessment")

# =====================================================
# INPUTS
# =====================================================

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 1, 120, 30)
    hypertension = st.selectbox(
        "Hypertension",
        [0, 1],
        format_func=lambda x: "No" if x == 0 else "Yes"
    )
    heart_disease = st.selectbox(
        "Heart Disease",
        [0, 1],
        format_func=lambda x: "No" if x == 0 else "Yes"
    )
    bmi = st.number_input("BMI", 10.0, 60.0, 25.0)
    hba1c = st.number_input("HbA1c", 3.0, 15.0, 5.5)
    blood_glucose = st.number_input("Blood Glucose", 50, 500, 100)

with col2:
    pregnancies = st.number_input("Pregnancies", 0, 20, 0)
    glucose = st.number_input("Glucose", 50, 300, 120)
    blood_pressure = st.number_input("Blood Pressure", 40, 200, 80)
    skin_thickness = st.number_input("Skin Thickness", 0, 100, 20)
    insulin = st.number_input("Insulin", 0, 900, 80)
    dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.5)

# =====================================================
# GENDER
# =====================================================

st.subheader("Gender")
gender = st.radio(
    "Select Gender",
    ["Female", "Male", "Other", "Unknown"]
)

gender_female = 1 if gender == "Female" else 0
gender_male = 1 if gender == "Male" else 0
gender_other = 1 if gender == "Other" else 0
gender_unknown = 1 if gender == "Unknown" else 0

# =====================================================
# SMOKING
# =====================================================

st.subheader("Smoking History")

smoking_map = {
    "Current": (1,0,0,0,0,0,0),
    "Ever": (0,1,0,0,0,0,0),
    "Former": (0,0,1,0,0,0,0),
    "Never": (0,0,0,1,0,0,0),
    "No Info": (0,0,0,0,1,0,0),
    "Not Current": (0,0,0,0,0,1,0),
    "Unknown": (0,0,0,0,0,0,1)
}

smoking_choice = st.selectbox(
    "Smoking Status",
    list(smoking_map.keys())
)

(
    current,
    ever,
    former,
    never,
    no_info,
    not_current,
    unknown
) = smoking_map[smoking_choice]

# =====================================================
# PAYLOAD
# =====================================================

payload = {
    "age": age,
    "hypertension": hypertension,
    "heart_disease": heart_disease,
    "bmi": bmi,
    "hba1c": hba1c,
    "blood_glucose": blood_glucose,
    "pregnancies": pregnancies,
    "glucose": glucose,
    "blood_pressure": blood_pressure,
    "skin_thickness": skin_thickness,
    "insulin": insulin,
    "dpf": dpf,
    "gender_female": gender_female,
    "gender_male": gender_male,
    "gender_other": gender_other,
    "gender_unknown": gender_unknown,
    "current": current,
    "ever": ever,
    "former": former,
    "never": never,
    "no_info": no_info,
    "not_current": not_current,
    "unknown": unknown
}

# =====================================================
# PREDICT BUTTON
# =====================================================

if st.button("🔍 Predict Diabetes"):
    try:
        with st.spinner("Running prediction..."):
            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                timeout=120
            )
            response.raise_for_status()          # raise HTTPError for bad status codes
            result = response.json()

        # Store prediction results in session state
        st.session_state["prediction_done"] = True
        st.session_state["prediction_result"] = result

        # Also store explanation (can be fetched after prediction)
        with st.spinner("Generating explanation..."):
            explain_response = requests.post(
                f"{API_URL}/explain",
                json=payload,
                timeout=120
            )
            explain_response.raise_for_status()
            explanation = explain_response.json()
        st.session_state["explanation"] = explanation

        st.success("Prediction Completed")

    except requests.exceptions.RequestException as e:
        st.error(f"API Connection Error: {e}")
        st.session_state["prediction_done"] = False
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        st.session_state["prediction_done"] = False

# =====================================================
# DISPLAY RESULTS (if prediction exists)
# =====================================================

if st.session_state.get("prediction_done", False):
    result = st.session_state["prediction_result"]

    st.subheader("Prediction Result")
    col1, col2, col3 = st.columns(3)
    col1.metric("Prediction", result["prediction"])
    col2.metric("Probability", f"{result['probability']:.2%}")
    col3.metric("Risk Level", result["risk_level"])

    st.write("### Risk Factors")
    for factor in result["risk_factors"]:
        st.write(f"• {factor}")

    # Display LangGraph explanation
    st.write("---")
    st.subheader("LangGraph Clinical Report")
    st.markdown(st.session_state["explanation"]["summary"])

    # =====================================================
    # GPT REPORT CHECKBOX (now works correctly)
    # =====================================================
    st.write("---")
    generate_gpt = st.checkbox("Generate GPT Clinical Report")

    if generate_gpt:
        with st.spinner("Generating GPT report..."):
            try:
                report_response = requests.post(
                    f"{API_URL}/report",
                    json=payload,
                    timeout=300
                )
                report_response.raise_for_status()
                report = report_response.json()
                st.subheader("GPT Clinical Report")
                st.markdown(report["report"])
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to generate GPT report: {e}")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("SmartGraphDx")
st.sidebar.info(
    """
    Model: GCN
    Retrieval:
    - ChromaDB
    - ADA
    - WHO
    - PubMed
    Agents:
    - Evidence Agent
    - Explanation Agent
    - Risk Agent
    - Lifestyle Agent
    - Monitoring Agent
    - Summary Agent
    LLM:
    - GPT-4o-mini
    Backend:
    - FastAPI
    Frontend:
    - Streamlit
    """
)
