# Development image: runs the checks and tests with the locked toolchain.
#
#   docker build -t pybuoy-dev .
#   docker run --rm pybuoy-dev                          # ./scripts/test
#   docker run --rm -v "$PWD:/app" pybuoy-dev ./scripts/lint
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Keep the virtual environment outside /app so mounting the source over it
# does not hide the installed dependencies.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project

COPY . .
RUN uv sync --locked

CMD ["./scripts/test"]
