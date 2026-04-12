import os
from env.generator import generate_patient
from env.evaluator import evaluator
from env.evolver import evolver

def test_ai_logic():
    print("--- [VERIFY] Testing Patient Generation ---")
    p = generate_patient("medium")
    print(f"Vignette: {p.vignette}")
    print(f"Symptoms: {p.symptoms}")
    print(f"Ground Truth Dept: {p.department}")
    
    print("\n--- [VERIFY] Testing Expert Evaluation ---")
    action = {"department": "cardiology", "seriousness": 4}
    ev = evaluator.evaluate(p.model_dump(), action)
    print(f"Score: {ev.get('score')}")
    print(f"Reasoning: {ev.get('reasoning')}")
    
    print("\n--- [VERIFY] Testing State Evolution ---")
    ev_next = evolver.evolve(p.model_dump(), waiting_time=5)
    print(f"Next Seriousness: {ev_next.get('true_seriousness')}")
    print(f"Next Vitals: {ev_next.get('vitals')}")

if __name__ == "__main__":
    if not os.getenv("HF_TOKEN"):
        print("ERROR: HF_TOKEN not set!")
    else:
        try:
            test_ai_logic()
        except Exception as e:
            print(f"Verification FAILED: {e}")
