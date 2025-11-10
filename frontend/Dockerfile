FROM ghcr.io/astral-sh/uv:python3.11-bookworm

WORKDIR /frontend

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# copie ton code (pages/, assets/ si tu en as)
COPY . .

EXPOSE 8501
CMD ["uv", "run", "streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
