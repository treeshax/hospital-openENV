# 🟢 EASY: only check priority
def grade_easy(patient, action):
    if action["priority"] == patient["true_priority"]:
        return 1.0
    return 0.0


# 🟡 MEDIUM: only check department
def grade_medium(patient, action):
    if action["department"] == patient["department"]:
        return 1.0
    return 0.0


# 🔴 HARD: both must be correct
def grade_hard(patient, action):
    if (
        action["priority"] == patient["true_priority"]
        and action["department"] == patient["department"]
    ):
        return 1.0
    return 0.0
