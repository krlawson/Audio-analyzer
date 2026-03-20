# 1. Start with a stable Python base
FROM python:3.11-slim

# 2. Install the system-level 'Headache' dependencies
# We added 'git' here so the container can push results back to you
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# 3. Create a workspace
WORKDIR /app

# 4. Install the Python science stack
RUN pip install --no-cache-dir \
    librosa \
    numpy \
    matplotlib \
    soundfile

# 5. Copy your Python script into the container
# We use '.' to ensure it's in the WORKDIR
COPY analyzer.py .

# 6. Set the script to run
# Using 'python' as the entrypoint allows the YAML to pass arguments
ENTRYPOINT ["python", "analyzer.py"]
