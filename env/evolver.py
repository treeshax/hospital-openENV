from env.llm import brain
from env.prompts import EVOLVER_SYSTEM_PROMPT
from typing import Dict, Any

class StateEvolver:
    def evolve(self, patient: Dict[str, Any], waiting_time: int) -> Dict[str, Any]:
        user_prompt = f"""
        ### CURRENT PATIENT STATE:
        Vignette: {patient.get('vignette')}
        Vitals: HR {patient.get('heart_rate')}, BP {patient.get('blood_pressure_sys')}/{patient.get('blood_pressure_dia')}, Temp {patient.get('temperature_c')}, O2 {patient.get('o2_saturation')}%
        Current Seriousness: {patient.get('true_seriousness')}
        
        ### QUEUE STATUS:
        Waiting Time: {waiting_time} steps.
        """
        
        result = brain.generate_json(EVOLVER_SYSTEM_PROMPT, user_prompt)
        return result

evolver = StateEvolver()
