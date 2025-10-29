

import streamlit as st
from audio_recorder_streamlit import audio_recorder
#import some gemini
import base64


    # initialize openai client def setup_openai_client(api_key):
    def setup_openai_client(api_key):

      return openai.OpenAI(api_key=api_key)

    # function to transcribe audio to text
    def transcribe_ audio(client,audio_path):

    with open audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model = "whisper-1", file=audio_file)
        return transcript.text

#taking response from OpenAI

    def fetch_ai_response(client,input_text):
        messages = [{"role":"user","content":input_text]
        response = client.chat.completions.create(model="gpt-3.5-turbo-1106",messages= messages)
        return response.choices[0].message.content

#convert text to audio

    def text_to_audio(client,text,audio_path):
        response=client.audio.speech.create(model="tts-1", voice="nova", input=text)
        response.stream_to_file(audio_path)

#auto-play audio function

    def auto_play_audio (audio_file):

        with open (audio _file, "rb") as audio_file:
            audio_bytes=audio_file.read()
        base64_audio=base64.b64encode (audio_bytes).decode("utf-8")
        audio_html - f'caudio src="data: audio/mp3;base64, (base64_audio)* contre
        st.markdown(audio_html, unsafe_allow_html=True)



def main():

    st.sidebar.title("API KEY CONFIGURATION")
    api_key = st.sidebar.text_input("Enter your API key", type="password")

    st.title("IDA ING")
    st.write("Hi there loyal customer of ING!How may I help you? Click on the voice recorder to interact with me!")
    recorded_audio = audio_recorder()

    #check if api key is there
    if api_key:
        client = setup_openai_client(api_key)
    recorded_audio = audio_recorder()
    # check if recording is done and available
    if recorded_audio:
        audio_file = "audio.mp3"
        with open(audio_file,"wb") as f:
            f.write(recorded_audio)

        transcribed_text =transcribe_audio(client, audio_file)
        st.write("Transcribed Text: ", transcribed_text)


        ai_response = fetch_ai_response(client, transcribed_text)
        response_audio_file = "audio_response.mp3"
        text_to_audio(client, ai_response, response_audio_file)
        st.audio(response_audio_file)
        st.write("AI Response:", ai_response)

if __name__ == "__main__":
    main()