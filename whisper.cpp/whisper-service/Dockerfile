FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential cmake git curl python3 python3-pip ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Clone and build whisper.cpp
RUN git clone https://github.com/ggerganov/whisper.cpp.git /opt/whisper.cpp && \
    cd /opt/whisper.cpp && \
    mkdir build && cd build && \
    cmake .. && \
    make -j && \
    cp bin/whisper-cli /usr/local/bin/whisper

# Download model
RUN mkdir -p /models && \
    cd /models && \
    curl -L -O https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin

# Install FastAPI + Uvicorn
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service
COPY app.py .

EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
