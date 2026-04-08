from pydantic import BaseModel, Field
from typing import List, Literal


class Patient(BaseModel):
    symptoms: List[str]

    age: int = Field(..., ge=0, le=120)
    heart_rate: int = Field(..., ge=30, le=220)
    blood_pressure: int = Field(..., ge=50, le=200)

    # ADD THESE (CRITICAL)
    true_seriousness: Literal[1, 2, 3, 4, 5]
    department: Literal[
        "cardiology",
        "neurology",
        "orthopedics",
        "pulmonology",
        "general",
        "emergency"
    ]


class Action(BaseModel):
    seriousness: Literal[1, 2, 3, 4, 5]

    department: Literal[
        "cardiology",
        "neurology",
        "orthopedics",
        "pulmonology",
        "general",
        "emergency"
    ]