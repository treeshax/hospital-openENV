from pydantic import BaseModel, Field
from typing import List, Literal


class Patient(BaseModel):
    vignette: str
    symptoms: List[str]
    age: int = Field(..., ge=0, le=120)
    
    # Advanced Vitals
    heart_rate: int = Field(..., ge=30, le=220)
    blood_pressure_sys: int = Field(..., ge=50, le=250)
    blood_pressure_dia: int = Field(..., ge=30, le=150)
    temperature_c: float = Field(..., ge=30.0, le=45.0)
    o2_saturation: int = Field(..., ge=50, le=100)
    respiratory_rate: int = Field(..., ge=5, le=60)

    # Ground Truth (for evaluation)
    true_seriousness: Literal[1, 2, 3, 4, 5]
    department: str
    is_contagious: bool = False
    
    # Meta
    waiting_time: int = 0


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