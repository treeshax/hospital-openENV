import json
from typing import Dict, Any, List
from .models import Action
from .evaluator import evaluator

def get_hospital_tools(env):
    """Returns a list of tools for the MCP server."""
    
    def list_patients():
        """List patients currently waiting for triage."""
        if not env.patient:
            return "No patients waiting."
        return f"Incoming Patient: 1 (Age: {env.patient.age})"

    def get_patient_details():
        """Get full medical vignette and symptoms for the current patient."""
        if not env.patient:
            return "No current patient."
        return {
            "vignette": env.patient.vignette,
            "symptoms": env.patient.symptoms,
            "age": env.patient.age,
            "vitals": {
                "heart_rate": env.patient.heart_rate,
                "bp": f"{env.patient.blood_pressure_sys}/{env.patient.blood_pressure_dia}",
                "temp": env.patient.temperature_c,
                "o2": env.patient.o2_saturation,
                "rr": env.patient.respiratory_rate
            }
        }

    def submit_triage(department: str, seriousness: int):
        """Submit the triage decision for the current patient."""
        action = {"department": department, "seriousness": seriousness}
        state, reward, done, info = env.step(action)
        return {
            "reward": reward,
            "done": done,
            "eval": info.get("eval"),
            "true_seriousness": info.get("true_seriousness")
        }

    def check_resources():
        """Check bed capacity and current load in all departments."""
        return env.get_queue_status()

    return {
        "list_patients": list_patients,
        "get_patient_details": get_patient_details,
        "submit_triage": submit_triage,
        "check_resources": check_resources
    }
