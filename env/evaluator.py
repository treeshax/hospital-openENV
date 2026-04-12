from env.llm import brain
from env.prompts import EVALUATOR_SYSTEM_PROMPT
from typing import Dict, Any

class ExpertEvaluator:
    def evaluate(self, patient: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
        user_prompt = f"""
        ### PATIENT DATA:
        Vignette: {patient.get('vignette')}
        Symptoms: {patient.get('symptoms')}
        Age: {patient.get('age')}
        Vitals: HR {patient.get('heart_rate')}, BP {patient.get('blood_pressure_sys')}/{patient.get('blood_pressure_dia')}, Temp {patient.get('temperature_c')}C, O2 {patient.get('o2_saturation')}% O2
        Contagious: {patient.get('is_contagious')}
        
        ### AGENT ACTION:
        Department: {action.get('department')}
        Seriousness: {action.get('seriousness')}
        """
        
        result = brain.generate_json(EVALUATOR_SYSTEM_PROMPT, user_prompt)
        return result

evaluator = ExpertEvaluator()
