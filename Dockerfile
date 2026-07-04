FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install python-dotenv fastapi uvicorn openai pydantic
CMD ["python3", "ark_orchestrator.py"]