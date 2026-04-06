# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir \
    pydantic \
    fastapi \
    uvicorn \
    openenv-core \
    openai

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "-m", "server.app"]