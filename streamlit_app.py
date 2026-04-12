import streamlit as st
import pandas as pd
import random
import time
import json
import sys
import os
from datetime import datetime

# Add root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from env.hospital_env import HospitalEnv
from env.models import Action

# Page Config
st.set_page_config(
    page_title="HOSPITAL WAR ROOM | AI-TRÍAGE",
    page_icon="🧬",
    layout="wide",
)

# Premium CSS for "Deep Space" Medical Logic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    :root {
        --primary: #3b82f6;
        --secondary: #10b981;
        --accent: #f43f5e;
        --bg-dark: #020617;
        --card-bg: rgba(30, 41, 59, 0.4);
    }

    .stApp {
        background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #020617 100%);
        font-family: 'Space Grotesk', sans-serif;
        color: #f8fafc;
    }

    /* Glassmorphism Navigation */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Professional Cards */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 40px -10px rgba(0,0,0,0.5);
    }

    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        letter-spacing: -1px;
        background: linear-gradient(135deg, #60a5fa 0%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Simulation Status Banner */
    .status-banner {
        padding: 8px 16px;
        border-radius: 200px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        display: inline-block;
        margin-bottom: 16px;
    }
    
    .status-live { background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.2); }
    .status-mci { background: rgba(244, 63, 94, 0.1); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.2); }

    /* Vignette Display */
    .vignette-box {
        background: rgba(0, 0, 0, 0.2);
        border-left: 4px solid var(--primary);
        padding: 20px;
        border-radius: 12px;
        margin: 16px 0;
        font-style: italic;
        line-height: 1.6;
        color: #cbd5e1;
    }

    .vital-chip {
        display: inline-block;
        background: rgba(255, 255, 255, 0.05);
        padding: 4px 12px;
        border-radius: 8px;
        margin-right: 8px;
        font-size: 0.85rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Hide standard UI clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Session State
if 'env' not in st.session_state:
    st.session_state.env = HospitalEnv(task="medium", max_steps=10)
    st.session_state.obs = st.session_state.env.reset()
    st.session_state.history = []
    st.session_state.total_reward = 0
    st.session_state.step_count = 0
    st.session_state.current_scenario = "Normal Operations"

# SIDEBAR
with st.sidebar:
    st.markdown('<h1 style="font-size: 1.5rem;">🧬 MISSION CONTROL</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    difficulty = st.select_slider("Simulation Intensity", ["Easy", "Medium", "Hard", "MCI", "Outbreak"], value="Medium")
    
    if st.button("REFORMAT ENVIRONMENT 🔄", use_container_width=True):
        st.session_state.env = HospitalEnv(task=difficulty.lower())
        st.session_state.obs = st.session_state.env.reset()
        st.session_state.history = []
        st.session_state.total_reward = 0
        st.session_state.step_count = 0
        st.session_state.current_scenario = f"{difficulty} Mode"
        st.rerun()

    st.markdown("---")
    st.markdown("### 📊 STATS")
    st.metric("Total Score", f"{st.session_state.total_reward:.2f}")
    st.metric("Patients Triaged", st.session_state.step_count)
    
    st.markdown("---")
    st.caption("AI-Native Hospital Triage v2.0-Alpha")

# MAIN WORKBENCH
col_status, col_empty = st.columns([1, 2])
with col_status:
    status_class = "status-mci" if "MCI" in st.session_state.current_scenario else "status-live"
    st.markdown(f'<div class="status-banner {status_class}">● {st.session_state.current_scenario}</div>', unsafe_allow_html=True)

st.title("🏥 Clinical Intelligence Workbench")

# 1. THE INCOMING PATIENT (The "Case")
v = st.session_state.obs
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("👤 CURRENT CASE ANALYSIS")
st.markdown(f'<div class="vignette-box">{v["vignette"]}</div>', unsafe_allow_html=True)

# Vitals Row
vitals = v["vitals"]
v_col1, v_col2, v_col3, v_col4, v_col5 = st.columns(5)
with v_col1: st.markdown(f'<div class="vital-chip">❤️ HR: {vitals["heart_rate"]}</div>', unsafe_allow_html=True)
with v_col2: st.markdown(f'<div class="vital-chip">🩸 BP: {vitals["bp"]}</div>', unsafe_allow_html=True)
with v_col3: st.markdown(f'<div class="vital-chip">🌡️ TEMP: {vitals["temp"]}C</div>', unsafe_allow_html=True)
with v_col4: st.markdown(f'<div class="vital-chip">🫁 O2: {vitals["o2"]}%</div>', unsafe_allow_html=True)
with v_col5: st.markdown(f'<div class="vital-chip">⏱️ RR: {vitals["rr"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 2. DECISION PANEL
left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🦾 AGERNT OVERRIDE / MANUAL TRIAGE")
    
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        dept = st.selectbox("Assign Department", ["cardiology", "neurology", "orthopedics", "pulmonology", "general", "emergency"])
    with t_col2:
        seriousness = st.slider("Severity Level", 1, 5, 3)
        
    if st.button("SUBMIT TRIAGE DECISION ⚡", type="primary", use_container_width=True):
        action = {"department": dept, "seriousness": seriousness}
        obs, reward, done, info = st.session_state.env.step(action)
        
        # Log to history
        st.session_state.history.insert(0, {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Patient": v["vignette"][:50] + "...",
            "Decision": f"{dept.upper()} ({seriousness})",
            "Expert Reward": f"{reward:+.2f}",
            "Evaluator Analysis": info.get("eval", {}).get("reasoning", "No analysis provided.")
        })
        
        st.session_state.total_reward += reward
        st.session_state.step_count += 1
        
        if not done:
            st.session_state.obs = obs
            st.rerun()
        else:
            st.success("SIMULATION COMPLETE")
            st.balloons()
            
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏥 RESOURCE LOAD")
    qs = v.get("queue_status", {})
    if qs:
        for dept, status in qs.items():
            st.write(f"**{dept.capitalize()}** ({status['count']}/{status['capacity']})")
            st.progress(status['count']/status['capacity'])
    else:
        st.info("No load data available.")
    st.markdown('</div>', unsafe_allow_html=True)

# 3. ACTIVITY LOG
if st.session_state.history:
    st.markdown("### 📋 CLINICAL ACTIVITY LOG")
    for log in st.session_state.history:
        with st.expander(f"{log['Time']} - {log['Decision']} (Reward: {log['Expert Reward']})"):
            st.write(f"**Vignette:** {log['Patient']}")
            st.write(f"**Expert Feedback:** {log['Evaluator Analysis']}")

st.markdown("---")
st.caption("AI-Powered Simulation Dashboard | OpenENV Protocol Compliant")
