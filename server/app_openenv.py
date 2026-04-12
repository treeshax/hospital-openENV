"""Professional OpenENV Server for Hospital Triage.
Exposes MCP tools and supports stateless HTTP/WebSocket sessions.
"""

import os
import uuid
import asyncio
import json
import inspect
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from openenv.core.env_server import create_app
from openenv.core.env_server.mcp_environment import get_server_tools

from env.hospital_env import HospitalEnv
from env.models import Action, Patient
from env.tools import get_hospital_tools

# Initialize the OpenENV App
app = create_app(
    HospitalEnv,
    Action,
    dict, # Observation type
    env_name="hospital-triage-env",
    max_concurrent_envs=10,
)

# --- MCP Tool Registration ---
# The OpenENV framework picks up tools from the environment.
# We will monkey-patch the tools into the environment instance 
# so 'get_server_tools' can find them.

_sessions: Dict[str, HospitalEnv] = {}

class ResetBody(BaseModel):
    difficulty: str = "medium"
    scenario: Optional[str] = None
    seed: Optional[int] = None

@app.post("/api/reset")
async def api_reset(body: ResetBody = Body(default_factory=ResetBody)):
    """OpenENV-style stateless reset."""
    env = HospitalEnv(task=body.difficulty)
    obs = env.reset()
    session_id = str(uuid.uuid4())
    _sessions[session_id] = env
    
    # Extract tools
    tools_dict = get_hospital_tools(env)
    tools_list = []
    for name, fn in tools_dict.items():
        tools_list.append({
            "name": name,
            "description": fn.__doc__ or "",
            "parameters": {} # Simplified for now
        })
        
    return {
        "session_id": session_id,
        "observation": obs,
        "tools": tools_list
    }

@app.post("/api/call_tool")
async def api_call_tool(session_id: str, tool_name: str, arguments: Dict[str, Any] = {}):
    env = _sessions.get(session_id)
    if not env:
        raise HTTPException(status_code=404, detail="Session not found")
        
    tools = get_hospital_tools(env)
    if tool_name not in tools:
        raise HTTPException(status_code=400, detail=f"Tool {tool_name} not found")
        
    result = tools[tool_name](**arguments)
    return {
        "result": result,
        "done": False, # Need to track this better
        "reward": 0.0  # Detailed reward in result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
