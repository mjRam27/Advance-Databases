# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy everything to the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Set environment variables from .env file (use docker-compose to load .env)
# NOTE: Do not hardcode secrets here

# Start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
