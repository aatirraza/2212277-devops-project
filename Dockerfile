# Use a slim official Python image for optimization
FROM python:3.12-slim

# Set environment variables to optimize Python inside containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a secure working directory
WORKDIR /app

# Create a secure non-root system user and group
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Leverage Docker layer caching for dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Adjust permissions so the non-root user owns the app directory
RUN chown -R appuser:appgroup /app

# Switch to the non-root user context
USER appuser

# Document that the container uses port 8000
EXPOSE 8000

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "app"]
