FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .
EXPOSE 8000
CMD ["uvicorn", "credit_risk_simulator.presentation.api:app", "--host", "0.0.0.0", "--port", "8000"]
