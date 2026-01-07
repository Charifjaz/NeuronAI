FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --verbose -r requirements.txt

# Verify installation
RUN python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')"
RUN which python
RUN python -m streamlit version

# Copy application
COPY . .

EXPOSE 8501

# Run with python -m to ensure it's in PATH
CMD ["python", "-m", "streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.fileWatcherType=none"]