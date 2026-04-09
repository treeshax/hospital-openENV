FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Clean up local environment artifacts if any
RUN rm -rf __pycache__ .pytest_cache

# Default command
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "7860"]