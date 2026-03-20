# Use a slim version of Python to keep it fast
FROM python:3.11-slim

# 1. Install the "Hidden" dependencies that cause the headaches
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# 2. Set the working directory
WORKDIR /app

# 3. Install the Python science stack
RUN pip install --no-cache-dir \
    librosa \
    numpy \
    scipy \
    soundfile \
    matplotlib

# 4. Copy your forensic script into the box
COPY analyze.py .

# 5. Run it
ENTRYPOINT ["python", "/app/analyze.py"]
