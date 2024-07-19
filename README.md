# spillmate-therapist-chatbot
Talk to Spillmate to spill your thoughts and get timely, personalised assistance and CBT support 🪴✨
## Tech Stack

- Streamlit UI
- OpenAI Whisper Model (Speech To Text Transcription)
- IBM Watson (Text To Speech Service)
- Google Gemini AI (LLM as the therapist)
- PyDub to convert .mp3 audio file to .wav

## Features

- **Push To Talk Feature:** Hold down the button, speak your thoughts, release, and Spillmate will reply.
- **Natural and Realistic Voice:** Now Spillmate - your friendly therapist - gets a voice! It's more intuitive and interactive!
- **Timely and Judgement-Free:** Your Spillmate Therapist has got better! Improved responses from our specialised AI LLM.

## To Set Up the App

1. ```git clone https://github.com/21-0075-disha/spillmate-therapist-chatbot.git``` : clone the repository
2. configure a Python virtual environment with ```python-venv```, ```anaconda``` or ```miniconda```
3. ```pip install -r requirements.txt``` : install all required libraries & frameworks
4. In the ```.env``` file, fill placeholders with required API Keys
5. ```streamlit run chat-app.py``` : to run the app

## Areas to Work On

- Selection of different voices for the user to choose before proceeding to the therapist
- Better text-to-speech and speech-to-text models to integrate with
- Better user experience for mobile devices
