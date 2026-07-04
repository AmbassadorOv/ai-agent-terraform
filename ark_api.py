from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio
import os

app = FastAPI()

class AgentRequest(BaseModel):
    agent_id: str
    platform: str

active_agents = []

@app.get("/status")
def get_status():
    return {"status": "ONLINE", "agents": active_agents}

@app.post("/recruit")
async def recruit_agent(request: AgentRequest, background_tasks: BackgroundTasks):
    active_agents.append({"id": request.agent_id, "platform": request.platform, "status": "BOOTING"})
    background_tasks.add_task(start_agent_logic, request.agent_id)
    return {"message": f"Agent {request.agent_id} recruitment initiated"}

async def start_agent_logic(agent_id):
    await asyncio.sleep(5)
    for agent in active_agents:
        if agent["id"] == agent_id:
            agent["status"] = "HEALTH"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)