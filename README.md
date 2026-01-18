# README do Script de Reconhecimento de Fala, Geração de Resposta e Síntese de Voz

Este script demonstra um fluxo de trabalho que envolve reconhecimento de fala, processamento de linguagem natural e síntese de voz. Ele permite que o usuário grave um áudio, transcreva-o, use a transcrição como entrada para um modelo de linguagem (GPT-4) e, em seguida, converta a resposta do modelo em áudio.

## Funcionalidades

1.  **Gravação de Áudio**: Grava áudio do microfone do usuário no navegador.
2.  **Transcriçaõ de Áudio**: Transcreve o áudio gravado para texto usando o modelo Whisper da OpenAI.
3.  **Geração de Resposta**: Envia a transcrição para o modelo GPT-4 da OpenAI para gerar uma resposta.
4.  **Síntese de Voz**: Converte a resposta textual do GPT-4 em áudio usando gTTS (Google Text-to-Speech).

## Como Usar

### 1. Definir o Idioma

A primeira célula define o idioma para o reconhecimento de fala e a síntese de voz. Por padrão, está configurado para português (`"pt"`).

```python
language = "pt"
```

### 2. Gravação de Áudio

A segunda célula contém a lógica para gravar áudio diretamente no Google Colab. Ela usa JavaScript para acessar o microfone do navegador e salvar o áudio como um arquivo `.wav`.

```python
# ... (código para gravação de áudio)

print("Recording...\n")
record_file = record()
display(Audio(record_file, autoplay=False))
```

Execute esta célula para iniciar a gravação. O áudio será salvo em `/content/request_audio.wav`.

### 3. Instalar OpenAI Whisper

Esta célula instala a biblioteca `openai-whisper` necessária para a transcrição.

```python
!pip install git+https://github.com/openai/whisper.git -q
```

### 4. Transcrever Áudio

Esta célula carrega um modelo Whisper (o modelo "small" é usado aqui) e transcreve o arquivo de áudio gravado. A transcrição é armazenada na variável `transcription`.

```python
import whisper

model = whisper.load_model("small")

result = model.transcribe(record_file, fp16=False, language=language)
transcription = result["text"]

print(transcription)
```

### 5. Instalar a Biblioteca OpenAI

Instala a biblioteca oficial da OpenAI para interagir com suas APIs.

```python
!pip install openai
```

### 6. Configurar Chave da API OpenAI

**IMPORTANTE**: Você precisa inserir sua chave da API da OpenAI nesta célula. Substitua `'chave da api'` pela sua chave real. **Não compartilhe sua chave de API publicamente.**

```python
import os

os.environ["OPENAI_API_KEY"] = 'chave da api'
```

### 7. Interagir com o GPT-4

Esta célula inicializa o cliente da OpenAI e envia a transcrição (ou uma pergunta hardcoded para demonstração) para o modelo GPT-4. A resposta do modelo é armazenada em `chatgpt_response`.

```python
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Poderia me informar o valor do dólar?"} # Conteúdo de exemplo
    ]
)

chatgpt_response = response.choices[0].message.content
print(chatgpt_response)
```

**Nota**: O notebook atual está usando uma pergunta hardcoded para o GPT-4 (`"Poderia me informar o valor do dólar?"`). Para usar a transcrição real, você precisaria modificar a linha `"content"` para `"content": transcription`.

### 8. Instalar gTTS

Instala a biblioteca gTTS para síntese de texto em fala.

```python
!pip install gTTS
```

### 9. Sintetizar e Reproduzir Resposta em Áudio

Finalmente, esta célula usa a gTTS para converter a `chatgpt_response` em um arquivo de áudio (`/content/response_audio.wav`) e o reproduz automaticamente.

```python
from gtts import  gTTS

gtts_object = gTTS(text=chatgpt_response, lang=language, slow=False)

response_audio = "/content/response_audio.wav"
gtts_object.save(response_audio)

display(Audio(response_audio, autoplay=True))
```

## Dependências

*   `IPython.display` (para `Audio`, `display`, `Javascript`)
*   `google.colab` (para `output`)
*   `base64`
*   `whisper` (instalado via pip)
*   `openai` (instalado via pip)
*   `gTTS` (instalado via pip)

Certifique-se de que todas as dependências estejam instaladas e que sua chave da API da OpenAI esteja configurada corretamente para que o script funcione como esperado.
