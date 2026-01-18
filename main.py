from IPython.display import Audio, display, Javascript
from google.colab import output
from base64 import b64decode
import whisper
import os
from openai import OpenAI
from gtts import  gTTS


os.environ["OPENAI_API_KEY"] = 'chave da api'
language = "pt"


RECORD = """
const sleep  = time => new Promise(resolve => setTimeout(resolve, time))
const b2text = blob => new Promise(resolve => {
  const reader = new FileReader()
  reader.onloadend = e => resolve(e.srcElement.result)
  reader.readAsDataURL(blob)
})
var record = time => new Promise(async resolve => {
  stream = await navigator.mediaDevices.getUserMedia({ audio: true })
  recorder = new MediaRecorder(stream)
  chunks = []
  recorder.ondataavailable = e => chunks.push(e.data)
  recorder.start()
  await sleep(time)
  recorder.onstop = async () =>{
    blob = new Blob(chunks)
    text = await b2text(blob)
    resolve(text)
  }
  recorder.stop()
})
"""

def record(sec=5):
  display(Javascript(RECORD))
  js_result = output.eval_js("record(%s)" % (sec * 1000))
  audio = b64decode(js_result.split(",")[1])
  file_name = "request_audio.wav"
  with open (file_name, "wb") as f:
    f.write(audio)
  return f"/content/{file_name}"

print("Recording...\n")
record_file = record()
display(Audio(record_file, autoplay=False))

model = whisper.load_model("small")

result = model.transcribe(record_file, fp16=False, language=language)
transcription = result["text"]

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Poderia me informar o valor do dólar?"}
    ]
)

chatgpt_response = response.choices[0].message.content
print(chatgpt_response)

gtts_object = gTTS(text=chatgpt_response, lang=language, slow=False)

response_audio = "/content/response_audio.wav"
gtts_object.save(response_audio)

display(Audio(response_audio, autoplay=True))