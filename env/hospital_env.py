from env.models import Action
from env.generator import generate_patient

from env.tasks import (
    easy_task_reward,
    medium_task_reward,
    hard_task_reward
)

from collections import defaultdict   # ✅ NEW


class HospitalEnv:

    def __init__(self, task="easy", max_steps=10):
        self.task = task
        self.max_steps = max_steps

        self.queue = []
        self.current_step = 0
        self.patient = None

        self.correct = 0
        self.total = 0

        # 🏥 NEW: department-wise queues
        self.department_queues = defaultdict(list)

    # RESET ENVIRONMENT
    def reset(self):
        import random

        self.queue = [generate_patient(self.task) for _ in range(self.max_steps)]
        random.shuffle(self.queue)

        self.current_step = 0
        self.correct = 0
        self.total = 0

        # 🧹 NEW: reset queues
        self.department_queues.clear()

        self.patient = self.queue.pop(0)

        return self.state()

    # FEATURE ENGINEERING
    def _compute_risk(self, patient):
        return {
            "high_heart_rate": patient.heart_rate > 120,
            "low_blood_pressure": patient.blood_pressure < 90,
            "elderly": patient.age > 65
        }

    # CURRENT STATE
    def state(self):
        risk = self._compute_risk(self.patient)

        return {
            "symptoms": self.patient.symptoms,
            "age": self.patient.age / 100,  # normalize
            "heart_rate": self.patient.heart_rate / 200,
            "blood_pressure": self.patient.blood_pressure / 200,

            # 🔥 important features
            "risk": risk,
            "difficulty": self.task,
            "progress": self.current_step / self.max_steps
        }

    # VALIDATE ACTION
    def _validate_action(self, action_dict):
        required_keys = ["seriousness", "department"]
        for key in required_keys:
            if key not in action_dict:
                raise ValueError(f"Missing key in action: {key}")

    # 🏥 NEW: PROCESS PATIENTS (simulate treatment)
    def process_patients(self):
        for dept in self.department_queues:
        # process only sometimes
            if self.department_queues[dept] and random.random() < 0.3:
                self.department_queues[dept].pop(0)
    # 🏥 NEW: QUEUE STATUS
    def get_queue_status(self):
        status = {}

        for dept, patients in self.department_queues.items():
            status[dept] = {
                "total": len(patients),
                "seriousness_levels": [p["seriousness"] for p in patients]
            }

        return status

    # STEP FUNCTION
    def step(self, action_dict):
        self._validate_action(action_dict)

        action = Action(**action_dict)

        # reward
        reward = self._get_reward(self.patient, action.model_dump())

        if action_dict["department"] == self.patient.department:
            reward += 1
            self.correct += 1
        else:
            reward -= 1

        self.total += 1
        self.current_step += 1

        current_patient = self.patient

        # 🏥 NEW: ADD PATIENT TO DEPARTMENT QUEUE
        dept = action_dict["department"]
        ser = action_dict["seriousness"]

        self.department_queues[dept].append({
            "patient": current_patient,
            "seriousness": ser
        })

        # 🔥 PRIORITY SORT (highest seriousness first)
        self.department_queues[dept].sort(
            key=lambda x: x["seriousness"],
            reverse=True
        )

        # 🏥 simulate treatment
        # self.process_patients()

        done = (len(self.queue) == 0) or (self.current_step >= self.max_steps)

        if not done:
            self.patient = self.queue.pop(0)
            next_state = self.state()
        else:
            next_state = None

        info = {
            "task": self.task,
            "true_seriousness": current_patient.true_seriousness,
            "true_department": current_patient.department,
            "agent_action": action_dict,
            "accuracy": self.correct / self.total if self.total > 0 else 0,
            "step": self.current_step,
            "reward": reward,

            # 🏥 NEW: queue snapshot
            "queue_status": self.get_queue_status()
        }

        return next_state, reward, done, info

    # REWARD ROUTER
    def _get_reward(self, patient, action):
        if self.task == "easy":
            return easy_task_reward(patient, action)

        elif self.task == "medium":
            return medium_task_reward(patient, action)

        elif self.task == "hard":
            return hard_task_reward(patient, action)

        else:
            raise ValueError(f"Unknown task: {self.task}")