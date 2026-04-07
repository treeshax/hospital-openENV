from env.hospital_env import HospitalEnv

MAX_STEPS = 20


def get_action(state):
    symptoms = " ".join(state["symptoms"]).lower()
    age = state["age"]
    hr = state["heart_rate"]
    bp = state["blood_pressure"]

    #  Department Scoring
    dept_scores = {
        "cardiology": 0,
        "pulmonology": 0,
        "neurology": 0,
        "orthopedics": 0,
        "emergency": 0,
        "general": 0
    }

    # weighted keywords
    if "chest pain" in symptoms:
        dept_scores["cardiology"] += 3
    if "palpitations" in symptoms:
        dept_scores["cardiology"] += 2

    if "breath" in symptoms or "cough" in symptoms:
        dept_scores["pulmonology"] += 2

    if "headache" in symptoms or "dizziness" in symptoms:
        dept_scores["neurology"] += 2

    if "fracture" in symptoms or "injury" in symptoms:
        dept_scores["orthopedics"] += 3

    if "bleeding" in symptoms or "trauma" in symptoms:
        dept_scores["emergency"] += 4

    # fallback
    dept_scores["general"] += 1

    # pick best department
    department = max(dept_scores, key=dept_scores.get)

    # Priority Scoring
    priority_score = 0

    # vitals (HIGH IMPACT)
    if hr > 130 or hr < 45:
        priority_score += 3

    if bp > 180 or bp < 80:
        priority_score += 3

    # symptoms severity
    if any(x in symptoms for x in ["unconscious", "severe", "chest pain"]):
        priority_score += 3
    elif any(x in symptoms for x in ["moderate", "pain", "fever"]):
        priority_score += 1

    # age risk
    if age > 70:
        priority_score += 1

    #  Convert score → priority
    if priority_score >= 4:
        priority = 3
    elif priority_score >= 2:
        priority = 2
    else:
        priority = 1

    if priority_score >= 4:
        seriousness = 3
    elif priority_score >= 2:
        seriousness = 2
    else:
        seriousness = 1
        
    return {
        "priority": priority,
        "department": department,
        "seriousness": seriousness
    }

def main():
    env = HospitalEnv(task="medium")
    state = env.reset()

    total_reward = 0

    for step in range(MAX_STEPS):
        action = get_action(state)

        next_state, reward, done, info = env.step(action)

        print(f"Step {step+1}")
        print("State:", state)
        print("Action:", action)
        print("Reward:", reward)
        print("-" * 30)

        total_reward += reward
        state = next_state

        if done:
            break

    print("Total Reward:", total_reward)


if __name__ == "__main__":
    main()