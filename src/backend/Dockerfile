# 1. Base Image
FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies and Python utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    build-essential \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && pip3 install gdown \
    && rm -rf /var/lib/apt/lists/*

# Create directory for model weights
RUN mkdir -p /app/tmp/model-weights

# 4. Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# 5. Set Working Directory
WORKDIR /app

# 6. Copy pyproject.toml and poetry.lock first (for caching)
COPY pyproject.toml poetry.lock* /app/
COPY src/backend /app/src/backend
COPY src/depth_estimation /app/src/depth_estimation

# 7. Install Dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# 8. Copy the entire src directory
# COPY src /app/src/

# 9. Create an entrypoint script
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# 10. Expose Port
EXPOSE 8000

# 11. Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

