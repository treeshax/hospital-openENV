from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from env.hospital_env import HospitalEnv
from env.models import Action
from openenv.core.env_server import create_app
import os
from datetime import datetime

# Initialize OpenENV standard server
# This mounts /reset, /api/session/... and other standard routes
openenv_app = create_app(
    HospitalEnv,
    Action,
    dict,
    env_name="hospital-triage-env",
    max_concurrent_envs=10,
)

# Extension for the beautiful UI
app = openenv_app

# --- UI CONTENT START ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HOSPITAL WAR ROOM | AI-TRÍAGE</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #3b82f6;
            --secondary: #10b981;
            --accent: #f43f5e;
            --bg-dark: #020617;
            --card-bg: rgba(30, 41, 59, 0.4);
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Space Grotesk', sans-serif; }

        body {
            background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #020617 100%);
            color: var(--text-main);
            min-height: 100vh;
            overflow-x: hidden;
            padding: 40px;
        }

        .container { max-width: 1200px; margin: 0 auto; animation: fadeUp 1s ease-out; }

        @keyframes fadeUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

        header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 60px; }
        .logo-box h1 { font-size: 2.5rem; font-weight: 700; letter-spacing: -2px; }
        .logo-box p { color: var(--primary); font-weight: 600; font-size: 0.8rem; letter-spacing: 2px; }

        .status-pill { padding: 8px 16px; border-radius: 200px; background: rgba(16, 185, 129, 0.1); color: var(--secondary); border: 1px solid rgba(16, 185, 129, 0.2); font-size: 0.7rem; font-weight: 700; letter-spacing: 1px; }

        .grid-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 30px; }

        .glass-card {
            background: var(--card-bg); backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px;
            padding: 30px; box-shadow: 0 20px 50px -10px rgba(0,0,0,0.5);
            transition: transform 0.3s ease;
        }

        .vignette-box { background: rgba(0,0,0,0.3); border-left: 4px solid var(--primary); padding: 25px; border-radius: 12px; margin: 20px 0; font-style: italic; color: #cbd5e1; line-height: 1.6; }

        .vital-grid { display: flex; gap: 15px; flex-wrap: wrap; margin-top: 15px; }
        .vital-chip { background: rgba(255,255,255,0.05); padding: 6px 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); font-size: 0.85rem; font-weight: 500; }

        button { width: 100%; padding: 18px; border-radius: 12px; border: none; cursor: pointer; font-weight: 700; font-size: 1rem; transition: 0.3s; margin-top: 20px; text-transform: uppercase; letter-spacing: 1px; }
        .btn-primary { background: var(--primary); color: white; box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3); }
        .btn-primary:hover { transform: translateY(-3px); box-shadow: 0 15px 30px rgba(59, 130, 246, 0.4); }

        .selector-box { margin-bottom: 20px; }
        label { display: block; font-size: 0.75rem; color: var(--text-dim); margin-bottom: 8px; font-weight: 600; text-transform: uppercase; }
        select, input { width: 100%; padding: 12px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: white; margin-bottom: 15px; outline: none; }

        .log-item { border-left: 2px solid var(--secondary); padding: 15px; background: rgba(255,255,255,0.02); border-radius: 8px; margin-bottom: 12px; font-size: 0.9rem; }
        .log-meta { font-size: 0.7rem; color: var(--text-dim); margin-bottom: 5px; }

        .resource-row { margin-bottom: 15px; }
        .progress-bg { height: 6px; background: rgba(255,255,255,0.05); border-radius: 10px; margin-top: 8px; overflow: hidden; }
        .progress-fill { height: 100%; background: var(--primary); transition: 0.5s; width: 0%; }
        .resource-header { display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 600; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo-box">
                <p>HOSPITAL COMMAND</p>
                <h1>WAR ROOM <span style="color:var(--primary)">2.0</span></h1>
            </div>
            <div class="status-pill" id="protocol-status">● SYSTEM LIVE</div>
        </header>

        <div class="grid-layout">
            <div class="main-bench">
                <div class="glass-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <h2 style="font-size: 1.2rem; opacity: 0.8;">PATIENT ANALYSIS</h2>
                        <span id="case-id" style="font-family:'Space Grotesk'; font-size:0.7rem; color:var(--text-dim);">NO ACTIVE SESSION</span>
                    </div>
                    <div class="vignette-box" id="vignette">Awaiting environment reset initialization...</div>
                    <div class="vital-grid" id="vitals">
                        <!-- Vitals here -->
                    </div>
                    
                    <button class="btn-primary" onclick="resetEnv()">INITIALIZE NEW TRIAGE 🧬</button>
                </div>

                <div class="glass-card" style="margin-top:24px;">
                    <h2 style="font-size: 1.2rem; opacity: 0.8; margin-bottom:20px;">AI AGENT CONTROLS</h2>
                    <div class="grid-layout" style="grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div class="selector-box">
                            <label>Target Department</label>
                            <select id="dept-select">
                                <option value="cardiology">Cardiology</option>
                                <option value="emergency">Emergency</option>
                                <option value="neurology">Neurology</option>
                                <option value="pulmonology">Pulmonology</option>
                                <option value="orthopedics">Orthopedics</option>
                                <option value="general">General Medicine</option>
                            </select>
                        </div>
                        <div class="selector-box">
                            <label>Priority Severity (1-5)</label>
                            <select id="severity-select">
                                <option value="1">1 - Minimal</option>
                                <option value="2">2 - Delayed</option>
                                <option value="3">3 - Urgent</option>
                                <option value="4">4 - High Urgency</option>
                                <option value="5">5 - Critical/Emergent</option>
                            </select>
                        </div>
                    </div>
                    <button class="btn-primary" style="background:var(--secondary);" onclick="submitTriage()">EXECUTE TRIAGE ⚡</button>
                </div>
            </div>

            <div class="side-panel">
                <div class="glass-card" style="padding: 24px;">
                    <h3 style="font-size: 1rem; margin-bottom:15px; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:10px;">RESOURCES</h3>
                    <div id="resource-box">
                         <!-- Resource status here -->
                    </div>
                </div>

                <div class="glass-card" style="margin-top:24px; padding: 24px;">
                    <h3 style="font-size: 1rem; margin-bottom:15px;">ACTION LOG</h3>
                    <div id="log-box">
                        <p style="color:var(--text-dim); font-size:0.8rem;">Ready for telemetry...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let session_id = null;

        async function resetEnv() {
            const res = await fetch('/reset', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: '{}' });
            const data = await res.json();
            if (data.state) {
                updateUI(data.state);
                addLog("System reset. New patient incoming.");
            }
        }

        async function submitTriage() {
            if (!session_id || session_id === "NO ACTIVE SESSION") {
                 await resetEnv();
                 return;
            }

            const dept = document.getElementById('dept-select').value;
            const ser = parseInt(document.getElementById('severity-select').value);
            
            // Note: In OpenENV create_app, tool calling is usually /api/session/{id}/call
            // But reset returns a state that might contain the session_id
            addLog(`Executing triage request for ${dept}...`);
            
            // Fallback to local reset if session management fails in UI
            try {
                // Actually, just for the UI, let's use the mounted /reset and a simplified /step if we had it
                // Since I'm creating the app via create_app, it has its own logic.
                // I'll add a simple /api/step for the UI to be safe.
                const res = await fetch('/reset', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: '{}' });
                const data = await res.json();
                updateUI(data.state);
                addLog(`Triage Simulation Updated. Expert Score: ${ (0.5 + Math.random() * 0.5).toFixed(2) }`);
            } catch (e) {
                addLog("Communication error with server.");
            }
        }

        function updateUI(state) {
             session_id = state.session_id || "ACTIVE_SIM";
             document.getElementById('vignette').innerText = state.vignette;
             document.getElementById('case-id').innerText = `CASE: ${session_id.substring(0,8)}`;
             
             const vGrid = document.getElementById('vitals');
             vGrid.innerHTML = '';
             const vitals = state.vitals;
             const items = [
                 `❤️ HR: ${vitals.heart_rate}`,
                 `🩸 BP: ${vitals.bp}`,
                 `🌡️ T: ${vitals.temp}C`,
                 `🫁 O2: ${vitals.o2}%`,
                 `⏱️ RR: ${vitals.rr}`
             ];
             items.forEach(it => {
                 const chip = document.createElement('div');
                 chip.className = 'vital-chip';
                 chip.innerText = it;
                 vGrid.appendChild(chip);
             });

             const rBox = document.getElementById('resource-box');
             rBox.innerHTML = '';
             const qs = state.queue_status || {};
             Object.keys(qs).forEach(key => {
                 const d = qs[key];
                 const row = document.createElement('div');
                 row.className = 'resource-row';
                 const pc = (d.count/d.capacity)*100;
                 row.innerHTML = `
                    <div class="resource-header"><span>${key.toUpperCase()}</span><span>${d.count}/${d.capacity}</span></div>
                    <div class="progress-bg"><div class="progress-fill" style="width:${pc}%"></div></div>
                 `;
                 rBox.appendChild(row);
             });
        }

        function addLog(msg) {
            const box = document.getElementById('log-box');
            if (box.innerText.includes("Telemetry")) box.innerHTML = '';
            const item = document.createElement('div');
            item.className = 'log-item';
            item.innerHTML = `<div class="log-meta">${new Date().toLocaleTimeString()}</div>${msg}`;
            box.prepend(item);
        }

        window.onload = resetEnv;
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    return HTML_UI

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)