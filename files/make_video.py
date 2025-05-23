import os
import sys
import json
from moviepy.editor import *
from whisper_timestamped import load_model, transcribe_timestamped

# 📥 Argumentos
text = sys.argv[1]
video_id = sys.argv[2]

# 🛣️ Caminhos
DIR = "/home/n8n/files"
AUDIO_PATH = f"{DIR}/audio_{video_id}.wav"
SUBS_PATH = f"{DIR}/subs_{video_id}.json"
VIDEO_PATH = f"{DIR}/video_{video_id}.mp4"
FONT_NAME = "Anton"

# 🧼 Corrige nomes com \n ou espaços extras
def sanitize_files(folder):
    for fname in os.listdir(folder):
        if fname.startswith("image_") and any(fname.endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
            clean = fname.strip().replace('\n', '').replace('\r', '')
            old_path = os.path.join(folder, fname)
            new_path = os.path.join(folder, clean)
            if old_path != new_path:
                os.rename(old_path, new_path)

sanitize_files(DIR)

# 🟡 Gera legendas
def generate_subtitles():
    model = load_model("base")
    result = transcribe_timestamped(model, AUDIO_PATH, language="pt")
    with open(SUBS_PATH, "w") as f:
        json.dump(result["segments"], f, ensure_ascii=False, indent=2)

# 🔡 Formata segmentos
def format_segments(path):
    with open(path, "r") as f:
        data = json.load(f)
    return [((seg["start"], seg["end"]), seg["text"]) for seg in data]

# 🟨 Cria clipes de texto
def create_text_clips(segments, width):
    clips = []
    for (start, end), txt in segments:
        txt_clip = TextClip(
            txt, fontsize=72, color="yellow", font=FONT_NAME,
            size=(width, None), method="caption", align="center"
        ).set_position("center").set_start(start).set_end(end)
        clips.append(txt_clip)
    return clips

# ▶️ Execução
print("🟡 Gerando legendas...")
generate_subtitles()
subs = format_segments(SUBS_PATH)

# 🖼️ Carrega imagens válidas 
IMGS_DIR = os.path.join(DIR, "imagens")

img_files = sorted([
    os.path.join(IMGS_DIR, f) for f in os.listdir(IMGS_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])


if not img_files:
    raise ValueError("Nenhuma imagem encontrada para compor o vídeo.")

# 🕒 Tempo por imagem
duration_total = subs[-1][0][1]
img_duration = duration_total / len(img_files)

# 🖼️ Cria clipes
img_clips = [
    ImageClip(img, duration=img_duration)
    .resize(height=1920)
    .on_color(size=(1080, 1920), color=(0, 0, 0), pos="center")
    for img in img_files
]

background = concatenate_videoclips(img_clips, method="compose")
text_clips = create_text_clips(subs, width=900)

# 🎬 Composição
final = CompositeVideoClip([background] + text_clips)
final = final.set_audio(AudioFileClip(AUDIO_PATH))

print("🎬 Renderizando...")
final.write_videofile(VIDEO_PATH, fps=24)
print("✅ Finalizado:", VIDEO_PATH)
