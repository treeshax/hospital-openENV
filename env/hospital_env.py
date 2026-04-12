from env.models import Action, Patient
from env.generator import generate_patient
from env.evaluator import evaluator
from env.evolver import evolver

from collections import defaultdict
import random


class HospitalEnv:
    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self, task="easy", max_steps=10):
        self.task = task
        self.max_steps = max_steps

        self.queue = []
        self.current_step = 0
        self.patient = None

        self.correct = 0
        self.total = 0

        # 🏥 Department-wise queues
        self.department_queues = defaultdict(list)
        self.bed_capacity = {
            "cardiology": 5,
            "neurology": 5,
            "orthopedics": 5,
            "pulmonology": 5,
            "general": 10,
            "emergency": 3
        }

    # RESET ENVIRONMENT
    def reset(self):
        # Initial queue generation
        self.queue = [generate_patient(self.task) for _ in range(self.max_steps)]
        
        self.current_step = 0
        self.correct = 0
        self.total = 0

        self.department_queues.clear()
        self.patient = self.queue.pop(0)

        return self.state()

    # CURRENT STATE
    def state(self):
        return {
            "vignette": self.patient.vignette,
            "symptoms": self.patient.symptoms,
            "age": self.patient.age,
            "vitals": {
                "heart_rate": self.patient.heart_rate,
                "bp": f"{self.patient.blood_pressure_sys}/{self.patient.blood_pressure_dia}",
                "temp": self.patient.temperature_c,
                "o2": self.patient.o2_saturation,
                "rr": self.patient.respiratory_rate
            },
            "difficulty": self.task,
            "progress": self.current_step / self.max_steps,
            "queue_status": self.get_queue_status()
        }

    # GET QUEUE STATUS
    def get_queue_status(self):
        status = {}
        for dept, patients in self.department_queues.items():
            status[dept] = {
                "count": len(patients),
                "capacity": self.bed_capacity.get(dept, 5),
                "overflow": len(patients) > self.bed_capacity.get(dept, 5)
            }
        return status

    # 🎯 STEP FUNCTION (CORE LOGIC)
    def step(self, action_dict):
        action = Action(**action_dict)
        current_patient = self.patient

        # 🧠 EXPERT EVALUATION (THE BRAIN)
        eval_result = evaluator.evaluate(current_patient.model_dump(), action.model_dump())
        reward = eval_result.get("score", 0.0)
        
        # LOGIC: ADMIT PATIENT
        dept = action.department
        self.department_queues[dept].append({
            "patient": current_patient,
            "admitted_step": self.current_step,
            "seriousness": action.seriousness
        })

        # 🔥 UPDATE QUEUES & EVOLVE STATE
        self._update_environment()

        self.current_step += 1
        done = (len(self.queue) == 0) or (self.current_step >= self.max_steps)

        if not done:
            self.patient = self.queue.pop(0)
            next_state = self.state()
        else:
            next_state = None

        info = {
            "eval": eval_result,
            "true_seriousness": current_patient.true_seriousness,
            "true_department": current_patient.department,
            "step": self.current_step,
            "reward": reward
        }

        return next_state, reward, done, info

    def _update_environment(self):
        # Evolve patients in queues (those not yet "treated")
        for dept, queue in self.department_queues.items():
            for entry in queue:
                patient = entry["patient"]
                wait = self.current_step - entry["admitted_step"]
                if wait > 0:
                    # Deterioration logic
                    evolution = evolver.evolve(patient.model_dump(), wait)
                    patient.heart_rate = evolution.get("vitals", {}).get("heart_rate", patient.heart_rate)
                    patient.true_seriousness = evolution.get("true_seriousness", patient.true_seriousness)