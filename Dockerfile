FROM python:3.9-slim

WORKDIR /app

# ---- System dependencies for WeasyPrint ----
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    gir1.2-glib-2.0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker cache optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Render uses port 8000
EXPOSE 8000

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Production WSGI server
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
