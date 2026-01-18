import os
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
from openai import OpenAI
from gtts import gTTS

# Configure sua chave da API
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Defina a variável de ambiente OPENAI_API_KEY com sua chave da API")
language = "pt"

# Função para gravar áudio
def record(sec=5, filename="request_audio.wav"):
    fs = 44100  # taxa de amostragem
    print("Gravando...")
    audio = sd.rec(int(sec * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)
    print("Gravação concluída.")
    return filename

# Grava 5 segundos de áudio
record_file = record(5)

# Transcreve com Whisper
model = whisper.load_model("small")
result = model.transcribe(record_file, fp16=False, language=language)
transcription = result["text"]
print("Transcrição:", transcription)

# Usa OpenAI para gerar resposta
client = OpenAI(api_key=OPENAI_API_KEY)
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": transcription}
    ]
)

chatgpt_response = response.choices[0].message.content
print("Resposta do ChatGPT:", chatgpt_response)

# Converte resposta em áudio com gTTS
gtts_object = gTTS(text=chatgpt_response, lang=language, slow=False)
response_audio = "response_audio.mp3"
gtts_object.save(response_audio)
print(f"Áudio salvo em: {response_audio}")