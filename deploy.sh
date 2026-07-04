#!/bin/bash
echo "[ARK] Igniting Omega Framework..."
pip install python-dotenv fastapi uvicorn openai pydantic
python3 ark_orchestrator.py &
python3 ark_api.py