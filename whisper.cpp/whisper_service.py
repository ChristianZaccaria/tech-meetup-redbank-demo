import os
import subprocess
import tempfile
import json
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

WHISPER_CPP_PATH = "./whisper.cpp"
BINARY_PATH = os.path.join(WHISPER_CPP_PATH, "build/bin/whisper-cli")
MODEL_PATH = os.path.join(WHISPER_CPP_PATH, "models/ggml-base.en.bin")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    out_path = tmp_path + ".json"
    cmd = [
        BINARY_PATH,
        "-m", MODEL_PATH,
        "-f", tmp_path,
        "-of", tmp_path,
        "-oj",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print("❌ Whisper.cpp failed:")
        print(proc.stderr)
        print(proc.stdout)
        raise RuntimeError(f"Whisper exited with code {proc.returncode}")

    with open(out_path) as f:
        result = json.load(f)

    text = " ".join([s["text"] for s in result["transcription"]])
    return {"text": text}
