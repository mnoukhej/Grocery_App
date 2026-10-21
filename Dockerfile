# ===================================================
# Dockerfile for Grocery Store Management System
# ===================================================

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    PYTHONPATH=/app/backend

# Set working directory
WORKDIR /app

# Install dependencies first (for optimal Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and assets
COPY backend/ ./backend/
COPY ui/ ./ui/
COPY database.sql .

# Expose application port
EXPOSE 5000

# Container healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/').read()" || exit 1

# Start Flask application server
CMD ["python", "backend/server.py"]

