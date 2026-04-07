from pydantic import BaseModel
from typing import List, Literal


class Patient(BaseModel):
    symptoms: List[str]   # ✅ FIXED
    age: int
    heart_rate: int
    blood_pressure: int


class Action(BaseModel):
    seriousness: Literal[1, 2, 3, 4, 5]   # ✅ bounded range
    department: Literal[
        "cardiology",
        "neurology",
        "orthopedics",
        "pulmonology",
        "general",
        "emergency"
    ]