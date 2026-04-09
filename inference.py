import os
import sys
import json
import time
from openai import OpenAI
from env.hospital_env import HospitalEnv

# ==============================
# 🔇 STRICT LOG CONTROL (CRITICAL)
# ==============================
old_stdout = sys.stdout
sys.stdout = sys.stderr

def print_log(msg):
    old_stdout.write(msg + "\n")
    old_stdout.flush()

def log_start(task, model):
    print_log(f"[START] task={task} env=hospital-env model={model}")

def log_step(step, action, reward, done, error="null"):
    print_log(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error}")

def log_end(success, steps, score, rewards):
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print_log(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}")

# ==============================
# 🔐 ENV SETUP
# ==============================
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-oss-120b:groq")
API_KEY = os.getenv("HF_TOKEN")

USE_LLM = True
if not API_KEY:
    USE_LLM = False

client = None
if USE_LLM:
    try:
        client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    except:
        client = None
        USE_LLM = False

# ==============================
# 🧠 HELPERS
# ==============================
def safe_parse(text):
    try:
        return json.loads(text)
    except:
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            return json.loads(text[start:end])
        except:
            return {}

def normalize_action(action):
    try:
        dept = action.get("department", "").lower().strip()
        allowed = {"cardiology","neurology","orthopedics","pulmonology","general","emergency"}

        if dept not in allowed:
            return fallback_policy({})

        seriousness = int(action.get("seriousness", 3))
        seriousness = max(1, min(5, seriousness))

        return {"department": dept, "seriousness": seriousness}
    except:
        return fallback_policy({})

def fallback_policy(state):
    symptoms = " ".join(state.get("symptoms", [])).lower()

    if "unconscious" in symptoms or "severe bleeding" in symptoms:
        return {"department": "emergency", "seriousness": 5}

    if "chest pain" in symptoms or "palpitations" in symptoms:
        return {"department": "cardiology", "seriousness": 4}

    if "shortness of breath" in symptoms or "cough" in symptoms:
        return {"department": "pulmonology", "seriousness": 3}

    if "head injury" in symptoms or "dizziness" in symptoms:
        return {"department": "neurology", "seriousness": 3}

    if "fracture" in symptoms:
        return {"department": "orthopedics", "seriousness": 3}

    return {"department": "general", "seriousness": 2}

# ==============================
# 🤖 LLM
# ==============================
def ask_llm(state):
    if not USE_LLM or client is None:
        return fallback_policy(state)

    prompt = f"""
Assign department and seriousness (1-5).

Symptoms: {state.get('symptoms', [])}
Age: {state.get('age', 0)}
Heart Rate: {state.get('heart_rate', 0)}
Blood Pressure: {state.get('blood_pressure', 0)}

Return JSON only.
"""

    try:
        res = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            timeout=5
        )

        text = (res.choices[0].message.content or "").strip()
        return normalize_action(safe_parse(text))

    except Exception:
        return fallback_policy(state)

# ==============================
# 🚀 MAIN
# ==============================
def run_inference():

    tasks = ["easy", "medium", "hard"]

    for task_name in tasks:

        log_start(task_name, MODEL_NAME)

        env = HospitalEnv(task=task_name, max_steps=5)
        state = env.reset()

        rewards = []
        done = False
        step = 1
        total_reward = 0.0
        error_msg = "null"

        try:
            while not done and step <= 5:

                action = ask_llm(state)

                state, reward, done, info = env.step(action)

                reward = (reward + 3) / 8
                reward = max(0.001, min(0.999, reward))

                rewards.append(reward)
                total_reward += reward

                log_step(step, action, reward, done)

                step += 1

        except Exception as e:
            error_msg = str(e).replace("\n", " ")
            done = True

        score = max(min(total_reward, 0.999), 0.001)
        success = done and score > 0

        log_end(success, len(rewards), score, rewards)

# ==============================
# ▶️ ENTRY
# ==============================
if __name__ == "__main__":
    try:
        run_inference()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)