# 1. Start with a stable Python base
FROM python:3.11-slim

# 2. Install the system-level 'Headache' dependencies
# These are the C-libraries that Python usually can't find on its own
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 3. Create a workspace
WORKDIR /app

# 4. Install the Python science stack
# We do this before copying code to speed up future builds (caching)
RUN pip install --no-cache-dir \
    librosa \
    numpy \
    matplotlib \
    soundfile

# 5. Copy your Python script into the container
COPY analyzer.py .

# 6. Set the script to run by default
# It expects a file path as an argument
ENTRYPOINT ["python", "analyzer.py"]
