FROM python:3.11-slim-bookworm

WORKDIR /app
COPY . .

# ✅ Add missing system libraries (esp. libnss3 for TLS)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libnss3 \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ✅ Install Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
