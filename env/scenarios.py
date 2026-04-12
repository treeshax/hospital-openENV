import random
from .generator import generate_patient

class ScenarioManager:
    @staticmethod
    def get_scenario(name: str, num_patients: int):
        if name == "mci":
            return ScenarioManager.mass_casualty_incident(num_patients)
        elif name == "outbreak":
            return ScenarioManager.viral_outbreak(num_patients)
        else:
            return [generate_patient("medium") for _ in range(num_patients)]

    @staticmethod
    def mass_casualty_incident(count: int):
        """Sudden influx of high-severity trauma cases."""
        patients = []
        for _ in range(count):
            p = generate_patient("hard")
            if random.random() < 0.7:
                p.true_seriousness = max(4, p.true_seriousness)
                if "trauma" not in p.vignette.lower():
                    p.vignette = "MCI Victim: " + p.vignette
            patients.append(p)
        return patients

    @staticmethod
    def viral_outbreak(count: int):
        """Series of patients with contagious symptoms."""
        patients = []
        for _ in range(count):
            p = generate_patient("medium")
            if random.random() < 0.6:
                p.is_contagious = True
                p.vignette = "Patient presenting with respiratory distress and dry cough. Significant travel history. " + p.vignette
                p.department = "isolation"
            patients.append(p)
        return patients
