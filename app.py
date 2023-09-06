import os
import whisper
import openai
from googletrans import Translator
from google.cloud import texttospeech
from dotenv import load_dotenv
load_dotenv() 


original_file = "YOURPATH"
translator = Translator()

# # model to transcript audio to text free
# model = whisper.load_model("medium")

# result = model.transcribe(original_file)

# text = result["text"]


# model to transcript audio to text (no free)
with open(original_file, "rb") as audio_file:
        transcript = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            api_key=os.environ.get("OPENAI_API_KEY")
        )
text = transcript.text

# translate to spanish
translate_text = translator.translate(text, src='en', dest='es')

#Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text=translate_text.text)

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="es-CO", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')
