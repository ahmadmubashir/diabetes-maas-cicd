from pydantic import BaseModel

class PatientInput(BaseModel):
    age: float
    hypertension: int
    heart_disease: int
    bmi: float
    hba1c: float
    blood_glucose: float
    pregnancies: float
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    dpf: float

    gender_female: int
    gender_male: int
    gender_other: int
    gender_unknown: int

    current: int
    ever: int
    former: int
    never: int
    no_info: int
    not_current: int
    unknown: int