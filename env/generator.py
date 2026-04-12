import random
from env.models import Patient


from env.llm import brain
from env.prompts import GENERATOR_SYSTEM_PROMPT
from env.models import Patient
import random

def generate_patient(task="easy"):
    # We ignore 'task' for the vignette generation to keep realism high, 
    # but we can adjust complexity in the prompt if needed.
    
    user_prompt = f"Target Difficulty: {task}. Generate a unique patient case."
    if task == "hard":
        user_prompt += " Include multiple comorbidities or conflicting symptoms."
    
    data = brain.generate_json(GENERATOR_SYSTEM_PROMPT, user_prompt)
    
    if not data:
        # Fallback to a very basic case if LLM fails
        return Patient(
            vignette="Patient arrives with mild chest pain.",
            symptoms=["chest pain"],
            age=45,
            heart_rate=80,
            blood_pressure_sys=120,
            blood_pressure_dia=80,
            temperature_c=37.0,
            o2_saturation=98,
            respiratory_rate=16,
            department="general",
            true_seriousness=2,
            is_contagious=False
        )

    # Map the nested vitals and other keys
    vitals = data.get("vitals", {})
    return Patient(
        vignette=data.get("vignette", ""),
        symptoms=data.get("symptoms", []),
        age=data.get("age", 40),
        heart_rate=vitals.get("heart_rate", 80),
        blood_pressure_sys=vitals.get("blood_pressure_sys", 120),
        blood_pressure_dia=vitals.get("blood_pressure_dia", 80),
        temperature_c=vitals.get("temperature_c", 37.0),
        o2_saturation=vitals.get("o2_saturation", 98),
        respiratory_rate=vitals.get("respiratory_rate", 16),
        department=data.get("true_department", "general"),
        true_seriousness=data.get("true_seriousness", 3),
        is_contagious=data.get("is_contagious", False)
    )