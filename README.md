# 🎥 Video Automation with n8n + Ollama + Whisper

Este projeto automatiza a criação de vídeos curtos e impactantes com frases, imagens, voz e legendas sincronizadas, ideal para redes sociais. Tudo funciona através de fluxos no [n8n](https://n8n.io/), combinando ferramentas open source de IA e edição multimídia.

---

## ⚙️ Requisitos

### 🧠 Modelos e IA

* **[Ollama](https://ollama.com/)**: Execução local de modelos LLM (ex: `llama3` ou `mistral`)
* **[Whisper (OpenAI)](https://github.com/openai/whisper)**: Transcrição de áudio e geração de legendas sincronizadas
* **[TTS - Text to Speech](https://github.com/coqui-ai/TTS)** (opcional): Leitura da frase com voz clonada ou sintética

### 🧰 Backend e Automação

* **[n8n](https://n8n.io/)**: Orquestração dos fluxos automatizados
* **[MoviePy](https://zulko.github.io/moviepy/)**: Geração e composição de vídeo com imagens, áudio e legendas
* **[FFmpeg](https://ffmpeg.org/)**: Renderização de vídeo (necessário para o MoviePy)
* **Python 3.10+** e bibliotecas:

  * `moviepy`
  * `whisper-timestamped`
  * `torch`, `torchaudio`
  * `gtts` ou `coqui-tts`
  * `Pillow`
  * `imageio`
  * `requests`

---

## 📁 Estrutura da Pasta

```
/files
├── audio.wav                # Gerado com TTS
├── audio.srt               # Legendas sincronizadas geradas pelo Whisper
├── final_video.mp4         # Vídeo final pronto para redes sociais
├── fonts/                  # Fontes customizadas usadas no vídeo
├── imagens/                # Imagens usadas como plano de fundo
├── make_video.py           # Script principal de montagem do vídeo
├── add_subtitles.py        # Script para adicionar legendas
├── run_video.sh            # Script shell de execução automática
```

---

## 🚀 Como rodar

1. Clone o projeto em um novo VPS ou máquina:

```bash
git clone https://github.com/Paulolinks/video-automation-n8n.git
```

2. Instale os requisitos:

```bash
cd video-automation-n8n
pip install -r requirements.txt
```

3. Certifique-se que o Ollama esteja rodando localmente com o modelo desejado (ex: `llama3`):

```bash
ollama run llama3
```

4. Execute a automação pelo n8n ou pelo script:

```bash
python3 make_video.py "Frase motivacional aqui" 001
```
