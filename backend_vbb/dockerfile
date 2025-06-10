FROM python:3.11-slim-bookworm

WORKDIR /app
COPY . .

# ✅ Add system libraries (required for Redis + TLS support)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libnss3 \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ✅ Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Run FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
