import streamlit as st
import pydub
import openai
import whisper
from io import BytesIO
from dotenv import load_dotenv
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
load_dotenv()
## To Initialize Whisper model for speech to text
model = whisper.load_model("base")

## To Initialize IBM Watson TTS model
authenticator = IAMAuthenticator(api_key)
tts_service = TextToSpeechV1(authenticator=authenticator)
tts_service.set_service_url(url)

## Define Function to transcribe audio
def transcribe_audio(audio_bytes):
    audio = pydub.AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")
    audio.export("temp.wav", format="wav")
    result = model.transcribe("temp.wav")
    return result["text"]

## Define Function to correct typo errors (spelling correction)
def correct_spelling(text):
    # Implement a basic spell correction algorithm or use a library
    from textblob import TextBlob
    corrected_text = str(TextBlob(text).correct())
    return corrected_text

## Define Function to get response from Gemini
def get_gemini_response(prompt):
    system_prompt = "You are a cognitive behavioral therapist giving therapy on chat."
    full_prompt = f"{system_prompt}\n{prompt}"
    
    response = requests.post(
        'https://api.google-gemini.com/v1/generate',  # Replace with actual API endpoint
        json={'prompt': full_prompt},
        headers={'Authorization': f'Bearer your_google_gemini_api_key'}  # Replace with your actual API key
    )
    response.raise_for_status()
    return response.json()['text']

## Define Function to convert text to speech using IBM Watson TTS
def text_to_speech(text):
    response = tts_service.synthesize(
        text,
        voice='en-US_AllisonV3Voice', ## as an example
        accept='audio/mp3'
    ).get_result()

    ## To Save the audio to a file
    audio_file = "response.mp3"
    with open(audio_file, 'wb') as audio:
        audio.write(response.content)

    ## To Read the audio file
    with open(audio_file, 'rb') as audio:
        audio_bytes = audio.read()

    return audio_bytes

## Streamlit Page
st.title("Talk to Spillmate - Your Friendly Therapist")

## Using JavaScript to record audio
st.markdown("""
    <script>
    const startRecording = () => {
        const button = document.getElementById("record-button");
        button.textContent = "Release to Stop";
        button.onclick = stopRecording;

        navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            const audioChunks = [];
            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks);
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                const downloadLink = document.createElement("a");
                downloadLink.href = audioUrl;
                downloadLink.download = "recording.mp3";
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);
            });

            mediaRecorder.start();

            const stopRecording = () => {
                mediaRecorder.stop();
                stream.getTracks().forEach(track => track.stop());
                button.textContent = "Push to Talk";
                button.onclick = startRecording;
            }
        });
    }
    </script>
    <button id="record-button" onclick="startRecording()">Push to Talk</button>
""", unsafe_allow_html=True)

## To upload recorded speech
uploaded_file = st.file_uploader("Upload your audio file", type=["mp3"])

if uploaded_file is not None:
    st.write("Processing audio...")
    audio_bytes = uploaded_file.read()

    ## Speech to Text
    transcription = transcribe_audio(audio_bytes)
    st.write("You said: ", transcription)

    ## Correct typos
    corrected_text = correct_spelling(transcription)
    st.write("Corrected text: ", corrected_text)

    ## To Get response from Gemini AI
    response_text = get_gemini_response(corrected_text)
    st.write("Therapist: ", response_text)

    ## To Convert response to speech
    response_audio = text_to_speech(response_text)
    st.audio(response_audio, format="audio/mp3")
