import random


SYMPTOMS_LIST = [
    ("chest pain", "cardiology"),
    ("head injury", "neurology"),
    ("fracture", "orthopedics"),
    ("shortness of breath", "pulmonology"),
    ("fever", "general"),
    ("unconscious", "emergency"),
    ("severe bleeding", "emergency"),
]


def generate_patient(task="easy"):

    # 🔁 STEP 1: Select symptoms based on task
    if task == "easy":
        selected = [random.choice(SYMPTOMS_LIST)]

    elif task == "medium":
        selected = random.sample(SYMPTOMS_LIST, 2)

    elif task == "hard":
        selected = random.sample(SYMPTOMS_LIST, random.randint(2, 4))

    else:
        raise ValueError("Invalid task level")

    symptoms = [s[0] for s in selected]
    departments = [s[1] for s in selected]

    # 🧠 STEP 2: Decide TRUE DEPARTMENT (multi-symptom logic)

    # 🔥 Priority rules (realistic combinations)
    if "unconscious" in symptoms or "severe bleeding" in symptoms:
        department = "emergency"

    elif "chest pain" in symptoms and "shortness of breath" in symptoms:
        department = "cardiology"

    elif "head injury" in symptoms:
        department = "neurology"

    elif "fracture" in symptoms:
        department = "orthopedics"

    elif "shortness of breath" in symptoms:
        department = "pulmonology"

    elif "fever" in symptoms:
        department = "general"

    else:
        # fallback
        department = departments[0]

    # 🧍 STEP 3: Create patient
    patient = {
        "symptoms": symptoms,  # ✅ NOW LIST
        "age": random.randint(20, 80),
        "heart_rate": random.randint(60, 140),
        "blood_pressure": random.randint(80, 160),
        "department": department
    }

    # 🧠 STEP 4: SERIOUSNESS SCORING
    score = 1

    # 🔴 Vital-based scoring
    if patient["heart_rate"] > 120:
        score += 2
    elif patient["heart_rate"] > 100:
        score += 1

    if patient["blood_pressure"] < 90:
        score += 2
    elif patient["blood_pressure"] < 100:
        score += 1

    # 🧠 Symptom-based scoring (loop for multi symptoms)
    for symptom in symptoms:
        if symptom in ["unconscious", "severe bleeding"]:
            score += 3
        elif symptom in ["chest pain", "shortness of breath"]:
            score += 2
        elif symptom in ["head injury"]:
            score += 2
        elif symptom in ["fracture"]:
            score += 1
        elif symptom in ["fever"]:
            score += 0

    # 👶 Age-based risk
    if patient["age"] > 65:
        score += 1

    # ✅ Final seriousness (1–5 scale)
    patient["true_seriousness"] = min(5, score)

    return patient