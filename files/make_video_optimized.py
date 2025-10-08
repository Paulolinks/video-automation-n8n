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
        if fname.startswith("image_") and any(fname.endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
            clean = fname.strip().replace('\n', '').replace('\r', '')
            old_path = os.path.join(folder, fname)
            new_path = os.path.join(folder, clean)
            if old_path != new_path:
                os.rename(old_path, new_path)

sanitize_files(DIR)

# 🟡 Gera legendas (otimizado para memória)
def generate_subtitles():
    print("🟡 Carregando modelo Whisper...")
    model = load_model("base")
    print("🟡 Transcrevendo áudio...")
    result = transcribe_timestamped(model, AUDIO_PATH, language="pt")
    
    with open(SUBS_PATH, "w") as f:
        json.dump(result["segments"], f, ensure_ascii=False, indent=2)
    
    # Limpa memória
    del model
    gc.collect()

# 🔡 Formata segmentos
def format_segments(path):
    with open(path, "r") as f:
        data = json.load(f)
    return [((seg["start"], seg["end"]), seg["text"]) for seg in data]

# 🟨 Cria clipes de texto (otimizado)
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

print(f"🖼️ Processando {len(img_files)} imagens...")

# 🖼️ Cria clipes (otimizado para memória)
img_clips = []
for i, img in enumerate(img_files):
    try:
        clip = ImageClip(img, duration=img_duration)
        clip = clip.resize(height=1920)
        clip = clip.on_color(size=(1080, 1920), color=(0, 0, 0), pos="center")
        img_clips.append(clip)
        
        # Limpa memória a cada 5 imagens
        if (i + 1) % 5 == 0:
            gc.collect()
            
    except Exception as e:
        print(f"⚠️ Erro ao processar imagem {img}: {e}")
        continue

if not img_clips:
    raise ValueError("Nenhuma imagem válida foi processada.")

print("🎬 Concatenando imagens...")
background = concatenate_videoclips(img_clips, method="compose")

# Limpa memória das imagens individuais
del img_clips
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
