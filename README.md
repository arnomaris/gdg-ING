# IDA Voice Assistant
A voice assistant for ING, developed as the winning solution at the AI Accelerate Hack hosted by the Google Developer Group KU Leuven.

## Overview

This project features a voice assistant tailored for ING, leveraging recent advances in large language models. Built in Python, the solution integrates speech recognition, natural language understanding, and text-to-speech to deliver a seamless conversational experience. The solution was developed and presented during a 10-hour hackathon challenge.

### Features
- Voice command handeling, transcription and synthesis
- RAG pipeline for context aware responses
- DuckDB as search backend
- Intuitive interface for easy interaction

### Hackathon Context
- Event: AI Accelerate Hack by Google Developer Group KU Leuven
- Case: ING
- Result: Winning project (1st place)
- Team size: 3 members
- Competing teams on case: 12
- Total partcipants: 200+

### Tech Stack
- Python
- Core Libraries: Google Gemini API, Hugging Face Transformers, DuckDB, Streamlit
- NLP: RAG pipeline

### What I learned during this Hackathon
- It was my first time creating an AI application, I gained a lot of insights.
- I learned how to quickly addapt to situations to ensure we could deliver a product in time.
- How to work together with team members from a very different background.

### What I would have implemented if I had more time
- Stream voice responses from Gemini instead of waiting for the full response.
- Pass only data from the customer that is required to answer the query, it currently passes all the customers information.
- Change the interface so it shows previous responses.

## Setup & Usage
1. Clone the repository.
```console
git clone https://github.com/arnomaris/gdg-ING.git
```
2. Install dependencies.
```console
pip install -r requirements.txt
```
3. (Optional) Create .env file with GEMINI_KEY entry.
You can get a gemini api key from https://aistudio.google.com/api-keys
4. Run app `streamlit run main.py`

_Note: You may encouter bugs, this was written in 10 hours with minimal bug fixes afterwards._
