# ==========================================================
# Base Image
# ==========================================================
FROM python:3.13-slim


# ==========================================================
# Python Environment Configuration
# ==========================================================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# ==========================================================
# Application Directory
# ==========================================================
WORKDIR /app


# ==========================================================
# System Dependencies
# ==========================================================
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*


# ==========================================================
# Python Dependencies
# ==========================================================
COPY requirements/ ./requirements/


# ==========================================================
# CPU PyTorch
# ==========================================================
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements/cpu.txt


# ==========================================================
# Application Dependencies
# ==========================================================
RUN pip install --no-cache-dir -r requirements/base.txt


# ==========================================================
# Project Configuration
# ==========================================================
COPY pyproject.toml .


# ==========================================================
# Application Source
# ==========================================================
COPY src/ ./src/
COPY data/ ./data/


# ==========================================================
# Runtime Directories
# ==========================================================
RUN mkdir -p /app/logs


# ==========================================================
# Network
# ==========================================================
EXPOSE 8000


# ==========================================================
# Container Health Check
# ==========================================================
HEALTHCHECK \
    --interval=30s \
    --timeout=10s \
    --start-period=60s \
    --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health', timeout=5)" || exit 1


# ==========================================================
# Application Startup
# ==========================================================
CMD ["python", "-m", "uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]