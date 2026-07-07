FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY scripts ./scripts
COPY data ./data
RUN pip install --no-cache-dir -e .[dev]
EXPOSE 8000
CMD ["uvicorn", "sovereignai.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
