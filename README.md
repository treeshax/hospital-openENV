---
title: Hospital Triage OpenEnv
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Smart Hospital: RL Management Dashboard

🏥 Smart Hospital: Adaptive Triage & Resource Optimization Environment

Smart Hospital is a real-world reinforcement learning environment designed to simulate hospital triage and resource allocation under uncertainty.

Unlike traditional rule-based systems, this environment challenges AI agents to make high-stakes decisions where incorrect prioritization can lead to severe penalties—mirroring real clinical trade-offs.

---

### 🚨 Problem

Modern hospitals face:

- Overcrowded emergency departments
- Limited staff and critical care resources
- High variability in patient severity
- Risk of under-triaging critical patients or overloading specialists

Current systems rely heavily on static triage protocols, which struggle under dynamic and uncertain conditions.

---

### 💡 Our Approach

We model hospital triage as a sequential decision-making problem, where an agent must:

- Assign patients to the correct department
- Estimate urgency (seriousness)
- Balance risk vs resource utilization
- Handle multi-symptom ambiguity
- Avoid critical misclassification penalties

---

### 🧠 Why Reinforcement Learning?

This is not just classification.

Agents must optimize:

- Long-term reward across multiple patients
- Trade-offs between accuracy and safety
- Risk-sensitive decisions (e.g., missing emergencies)
- Performance under distribution shifts (easy → hard tasks)

This makes RL a natural fit for:

- Adaptive triage policies
- Robust decision-making under uncertainty
- Learning from simulated clinical environments

----

## ⚙️ Environment Design

###  Observation Space
- Symptoms (multi-label)
- Age and vitals (normalized)
- Risk indicators (derived features)
- Task difficulty and progression

###  Action Space
- Department selection (6 specialties)
- Seriousness level (1–5)

###  Reward System
- Partial credit for near-correct decisions
- Heavy penalties for critical misclassification
- Risk-aware shaping based on vitals and age

---

## 📊 Tasks

| Task   | Objective                              |
|--------|----------------------------------------|
| Easy   | Department prediction                  |
| Medium | Department + seriousness               |
| Hard   | Full triage with risk-aware penalties  |

---

## 🤖 Baseline Agent

We provide a hybrid agent combining:

- Rule-based medical priors  
- LLM-based reasoning  
- Fallback safety policies  

This ensures robustness even under API or model failures.

---

## 🧪 Evaluation

Agents are evaluated on:

- Accuracy across tasks  
- Risk-sensitive decision quality  
- Stability under uncertainty  
- Final normalized score (0–1)  


## 🌍 Real-World Impact

This system is designed as a **decision-support layer**, not a replacement for clinicians.

### Potential Applications:
- Emergency triage assistance  
- Hospital load balancing simulations  
- Training environments for AI in healthcare  
- Stress-testing healthcare policies under demand spikes  

---

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)**: For building the premium, glassmorphic dashboard UI.
- **[Python](https://www.python.org/)**: The engine behind the simulation and RL environment.
- **[Pydantic](https://docs.pydantic.dev/)**: Ensuring robust data validation for patients and agent actions.
- **[Pandas](https://pandas.pydata.org/)**: Handling time-series data for metrics and activity logging.

## 🏗️ Project Structure

- `env/`: Contains the core RL environment logic (`hospital_env.py`), data models (`models.py`), and reward functions (`rewards.py`).
- `scripts/`:
    - `dashboard.py`: The interactive Streamlit dashboard.
    - `run_baseline.py`: CLI-based baseline agent execution.
- `data/`: Sample patient datasets (`patients.json`).

## 🚦 How to Run

### 1. Install Dependencies
```bash
python3 -m pip install streamlit pydantic pandas
```

### 2. Launch the Dashboard
```bash
streamlit run scripts/dashboard.py
```
### 3. Launch on CLI
```bash
.venv/bin/python -m scripts.run_baseline
```
## 🧠 Dashboard Core Panels

- **🏥 Hospital State**: Live view of bed availability, staff allocation progress, and the current patient queue.
- **🤖 Agent Decisions**: Instant feedback on the agent's latest action, comparing its choice with the ground truth outcome.
- **📊 Real-time Metrics**: Tracking Total Reward, Avg Reward, and System Throughput.
- **🎮 Controls**: Step-by-step simulation or full episode automation.

---

## Hugging-Face link 

https://huggingface.co/spaces/abhinavvsingh/vaats

## Docker container ID 

e33b36d2810c3201754dc48d92c8c9eb1d08fe7b8c2f82a1d56ff5be57bfbcac

## UI Preview (Draft)
<img width="1512" height="858" alt="Screenshot 2026-04-05 at 5 25 47 AM" src="https://github.com/user-attachments/assets/320e6b44-ee41-4d71-8a65-f5d4e812b7c1" />




---
Built with ❤️ for AI research and hospital efficiency.
