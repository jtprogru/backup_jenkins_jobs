FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

COPY jenkins-backup.py ./

RUN useradd --uid 1000 --create-home app \
    && mkdir /backup \
    && chown app:app /backup

USER app

ENV PATH="/app/.venv/bin:$PATH" \
    JENKINS_JOBS_DIR=/backup

CMD ["python", "jenkins-backup.py"]
