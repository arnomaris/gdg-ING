import os
import wave
import librosa
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
import asyncio
import io
import soundfile as sf

from chatbot.database import retrieve_relevant_info, get_customer, get_customer_data

parent_dir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(parent_dir, '.env')
load_dotenv(dotenv_path)

def setup_client(api_key):
    return genai.Client(api_key=api_key)

async def fetch_ai_response(client, language, turns, relevant_info, customer_data, products, transactions):
    """
    Fetch AI chat response audio from Gemini Live chat.
    'turns' is a list of dicts with format:
    [{"role": "user" or "assistant", "parts": [{"text": "..."}]}, ...]
    """

    audio_buffer = io.BytesIO()
    wf = wave.open(audio_buffer, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)

    prompt = f"""You are a helpful ING Belgium banking assistant. 
        You help customers with:
        - Finding account information and balances
        - Explaining banking products and services  
        - Guiding through banking processes
        - Answering questions about transactions

        Always be professional, concise, and customer-friendly. 
        When speaking, use natural conversational language without emojis or bullet points.
        Speak clearly in the customer's preferred language (Dutch, French, or English).

        The following relevant information is supplied to you:
        {'\n'.join(relevant_info)}
        
        And the following information from the customer:
        {str(customer_data)}
        
        products:
        {'\n'.join([str(p) for p in products])}
        
        transactions:
        {'\n'.join([str(t) for t in transactions])}
        
        When asked about transactions, use data as ordering.
        
        Never give information if the customer_id does not match with the provided data.
    """

    language_code = 'nl-Nl'
    if language == 'nl':
        language_code = 'nl-NL'
    elif language == 'fr':
        language_code = 'fr-Fr'
    elif language == 'en':
        language_code = 'en-US'

    config = types.LiveConnectConfig(
        response_modalities = ["AUDIO"],
        speech_config = types.SpeechConfig(language_code=language_code),
        system_instruction = prompt,
        output_audio_transcription = {},
    )

    async with client.aio.live.connect(model="gemini-live-2.5-flash-preview", config=config) as session:
        # Send chat turns in one message
        await session.send_client_content(
            turns=turns,
            turn_complete=True,
        )

        async for response in session.receive():
            if response.data is not None:
                wf.writeframes(response.data)
            if response.server_content.output_transcription is not None:
                st.session_state.conversation.append({
                    "role": "model",
                    "parts": [{"text": response.server_content.output_transcription.text}]
                })

    wf.close()
    audio_buffer.seek(0)
    return audio_buffer.read()



async def transcribe_audio_stream(client, audio_bytes: bytes):
    """Transcribe audio using regular Gemini API (not Live API)."""

    # Convert audio to required format (16-bit PCM, 16kHz, mono)
    buffer = io.BytesIO(audio_bytes)
    y, sr = librosa.load(buffer, sr=16000, mono=True)

    # Convert to WAV format
    wav_buffer = io.BytesIO()
    sf.write(wav_buffer, y, 16000, format='WAV', subtype='PCM_16')
    wav_buffer.seek(0)
    converted_audio_bytes = wav_buffer.read()

    # Use regular Gemini API for transcription (not Live API)
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            "Please transcribe this audio and return only the transcribed text.",
            {
                "inline_data": {
                    "mime_type": "audio/wav",
                    "data": converted_audio_bytes
                }
            }
        ]
    )

    return response.text.strip()

iteration = 0
def main():
    if not os.getenv("GEMINI_KEY"):
        st.sidebar.title("API KEY CONFIGURATION")
        api_key = st.sidebar.text_input("Enter your API key", type="password")
    else:
        api_key = os.getenv("GEMINI_KEY")

    customer_id = st.sidebar.text_input("Klantnummer", type="default")

    st.title("IDA Voice Assistant")
    language = st.selectbox(
        "Language?",
        ("en", "fr", "nl"),
    )

    result = get_customer_data(customer_id)
    if result is None:
        return
    customer_data, products, transactions = result[0], result[1], result[2]
    st.write("Hi there! How may I help you? Click on the audio recorder to interact with me!")

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if api_key:
        client = setup_client(api_key)
        audio_bytes = st.audio_input("Record a voice message", sample_rate=16000, key="voice_input")

        if audio_bytes:
            with st.spinner("Thinking"):
                transcription = asyncio.run(transcribe_audio_stream(client, audio_bytes.getvalue()))

            if transcription:
                st.write("**You:**", transcription)
                st.session_state.conversation.append({
                    "role": "user",
                    "parts": [{"text": transcription}]
                })

                relevant = retrieve_relevant_info(transcription, language)
                with st.spinner("Answering"):
                    ai_response = asyncio.run(fetch_ai_response(client, language, st.session_state.conversation, relevant, customer_data, products, transactions))
                    st.audio(ai_response, format="audio/wav")


if __name__ == "__main__":
    main()
