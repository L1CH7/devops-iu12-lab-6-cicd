# --- Stage 1: builder ---
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /build

# Copy only pyproject.toml first for layer caching
COPY pyproject.toml .

# Install production deps only (no dev extras)
RUN uv sync --no-dev --frozen 2>/dev/null || uv sync --no-dev

COPY src/ ./src/

# --- Stage 2: production ---
FROM python:3.12-slim AS production

WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /build/.venv /app/.venv
COPY --from=builder /build/src ./src/

# Non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

ENV PATH="/app/.venv/bin:$PATH"
ENV FLASK_APP=src/app.py
ENV PYTHONPATH=/app
ENV FLASK_ENV=production

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
