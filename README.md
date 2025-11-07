# tech-meetup-redbank-demo
Red Bank Demo for Waterford Tech Meetup. This whole demo runs locally on your computer. It's been tested on Mac, but can work on other OS with a few minor changes.

## 1. Prerequisites
1. Install [Ollama](https://ollama.com/), and download the Qwen 2.5:3b AI model.
2. Run from the root of this repository: `pip install -r requirements.txt`

## 2. Deploy LlamaStackDistribution
1. Run: `OLLAMA_URL=http://localhost:11434 llama stack run starter`

## 3. Deploy Whisper
1. Run: `cd whisper.cpp`
2. Run: `uvicorn whisper_service:app --host 0.0.0.0 --port 8000`

## 4. Run through the Jupyter Notebook
1. Open the `redbank-demo-notebook.ipynb` notebook and run through each cell to experiment.
