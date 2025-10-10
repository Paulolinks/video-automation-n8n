import os
import sys
import json
import gc
from moviepy.editor import *
from whisper_timestamped import load_model, transcribe_timestamped

# 📥 Argumentos
text = sys.argv[1]
video_id = sys.argv[2]
font_name = sys.argv[3] if len(sys.argv) > 3 else "Anton"

# 🛣️ Caminhos
DIR = "/home/n8n/files"
AUDIO_PATH = f"{DIR}/audio_{video_id}.wav"
SUBS_PATH = f"{DIR}/subs_{video_id}.json"
VIDEO_PATH = f"{DIR}/video_{video_id}.mp4"
FONT_NAME = font_name

# 🧼 Corrige nomes com \n ou espaços extras
def sanitize_files(folder):
    for fname in os.listdir(folder):
        if fname.startswith("video_") and any(fname.endswith(ext) for ext in [".mp4", ".avi", ".mov", ".mkv"]):
            clean = fname.strip().replace('\n', '').replace('\r', '')
            old_path = os.path.join(folder, fname)
            new_path = os.path.join(folder, clean)
            if old_path != new_path:
                os.rename(old_path, new_path)

sanitize_files(DIR)

# 🟡 Gera legendas
def generate_subtitles():
    print("🟡 Carregando modelo Whisper...")
    model = load_model("base")
    print("🟡 Transcrevendo áudio...")
    result = transcribe_timestamped(model, AUDIO_PATH, language="pt")
    
    with open(SUBS_PATH, "w") as f:
        json.dump(result["segments"], f, ensure_ascii=False, indent=2)
    
    del model
    gc.collect()

# 🔡 Formata segmentos
def format_segments(path):
    with open(path, "r") as f:
        data = json.load(f)
    return [((seg["start"], seg["end"]), seg["text"]) for seg in data]

# 🟨 Cria clipes de texto
def create_text_clips(segments, width):
    clips = []
    for (start, end), txt in segments:
        try:
            txt_clip = TextClip(
                txt, fontsize=72, color="yellow", font=FONT_NAME,
                size=(width, None), method="caption", align="center"
            ).set_position("center").set_start(start).set_end(end)
            clips.append(txt_clip)
        except Exception as e:
            print(f"⚠️ Erro ao criar legenda: {e}")
            continue
    return clips

# ▶️ Execução
print("🟡 Gerando legendas...")
generate_subtitles()
subs = format_segments(SUBS_PATH)

# 🎬 Carrega vídeos válidos
VIDEOS_DIR = os.path.join(DIR, "videos")

video_files = sorted([
    os.path.join(VIDEOS_DIR, f) for f in os.listdir(VIDEOS_DIR)
    if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))
])

if not video_files:
    raise ValueError("Nenhum vídeo encontrado para compor o vídeo final.")

# 🕒 Tempo por vídeo
duration_total = subs[-1][0][1]
video_duration = duration_total / len(video_files)

print(f"🎬 Processando {len(video_files)} vídeos...")

# 🎬 Cria clipes de vídeo
video_clips = []
for i, video in enumerate(video_files):
    try:
        clip = VideoFileClip(video)
        # Redimensiona para 1080x1920 (vertical)
        clip = clip.resize(height=1920)
        # Centraliza no frame
        clip = clip.on_color(size=(1080, 1920), color=(0, 0, 0), pos="center")
        # Define duração
        clip = clip.set_duration(video_duration)
        video_clips.append(clip)
        
        # Limpa memória a cada 3 vídeos
        if (i + 1) % 3 == 0:
            gc.collect()
            
    except Exception as e:
        print(f"⚠️ Erro ao processar vídeo {video}: {e}")
        continue

if not video_clips:
    raise ValueError("Nenhum vídeo válido foi processado.")

print("🎬 Concatenando vídeos...")
background = concatenate_videoclips(video_clips, method="compose")

# Limpa memória dos vídeos individuais
del video_clips
gc.collect()

print("🟨 Criando legendas...")
text_clips = create_text_clips(subs, width=900)

# 🎬 Composição final
print("🎬 Compondo vídeo final...")
final = CompositeVideoClip([background] + text_clips)
final = final.set_audio(AudioFileClip(AUDIO_PATH))

# Limpa memória
del background
del text_clips
gc.collect()

print("🎬 Renderizando...")
final.write_videofile(
    VIDEO_PATH, 
    fps=24,
    codec='libx264',
    audio_codec='aac',
    temp_audiofile='temp-audio.m4a',
    remove_temp=True,
    verbose=False,
    logger=None
)

# Limpa memória final
del final
gc.collect()

print("✅ Finalizado:", VIDEO_PATH)
