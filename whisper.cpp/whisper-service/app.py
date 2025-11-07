import os
import subprocess
import tempfile
import json
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

BINARY_PATH = "/usr/local/bin/whisper"
MODEL_PATH = "/models/ggml-base.en.bin"

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # Write the uploaded file to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    out_path = tmp_path + ".json"

    # Whisper.cpp command — ffmpeg handles mp3/wav/m4a etc.
    cmd = [
        BINARY_PATH,
        "-m", MODEL_PATH,
        "-f", tmp_path,
        "-of", tmp_path,
        "-oj",                # output JSON
        "-otxt",              # also output .txt (optional but handy)
        "-nt",                # no timestamps (faster for plain text)
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.returncode != 0:
        print("❌ Whisper.cpp failed:")
        print(proc.stderr)
        print(proc.stdout)
        raise RuntimeError(f"Whisper exited with code {proc.returncode}")

    with open(out_path) as f:
        result = json.load(f)

    # Combine all text segments
    text = " ".join([s["text"].strip() for s in result["transcription"]])
    return {"text": text}
