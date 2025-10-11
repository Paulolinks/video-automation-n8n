from flask import Flask, request, jsonify, send_file
import os
import json
import sys
from gtts import gTTS
from moviepy.editor import *
from whisper_timestamped import load_model, transcribe_timestamped

# ========================================
# CONFIGURAÇÕES
# ========================================
app = Flask(__name__)

# Diretórios (ajuste conforme seu VPS)
BASE_DIR = "/home/n8n/files"
IMGS_DIR = os.path.join(BASE_DIR, "imagens")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
VOICE_SAMPLE = os.path.join(BASE_DIR, "voice_sample.wav")
FONT_NAME = "Anton"  # Você pode adicionar seleção de fonte depois

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def sanitize_image_files():
    """Remove espaços e quebras de linha dos nomes de arquivos"""
    if not os.path.exists(IMGS_DIR):
        return
    for fname in os.listdir(IMGS_DIR):
        if fname.startswith("image_") and any(fname.endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
            clean = fname.strip().replace('\n', '').replace('\r', '')
            old_path = os.path.join(IMGS_DIR, fname)
            new_path = os.path.join(IMGS_DIR, clean)
            if old_path != new_path:
                os.rename(old_path, new_path)

def generate_audio(text, audio_id):
    """Gera áudio com gTTS (Google Text-to-Speech)"""
    audio_path = f"{BASE_DIR}/audio_{audio_id}.wav"
    
    print(f"🎤 Gerando áudio para ID: {audio_id}")
    
    # Gera áudio com gTTS
    tts = gTTS(text=text, lang='pt', slow=False)
    tts.save(audio_path)
    
    print(f"✅ Áudio criado: {audio_path}")
    return audio_path

def generate_subtitles(audio_path, subs_path):
    """Gera legendas com timestamps usando Whisper"""
    print("📝 Gerando legendas...")
    model = load_model("base")
    result = transcribe_timestamped(model, audio_path, language="pt")
    
    with open(subs_path, "w") as f:
        json.dump(result["segments"], f, ensure_ascii=False, indent=2)
    
    # Formata segmentos
    segments = [((seg["start"], seg["end"]), seg["text"]) for seg in result["segments"]]
    print(f"✅ {len(segments)} segmentos de legenda criados")
    return segments

def create_text_clips(segments, width):
    """Cria clipes de texto para as legendas"""
    clips = []
    for (start, end), txt in segments:
        txt_clip = TextClip(
            txt, fontsize=72, color="yellow", font=FONT_NAME,
            size=(width, None), method="caption", align="center"
        ).set_position("center").set_start(start).set_end(end)
        clips.append(txt_clip)
    return clips

def create_video(audio_path, video_id):
    """Cria vídeo com imagens, áudio e legendas"""
    print("🎬 Criando vídeo...")
    
    subs_path = f"{BASE_DIR}/subs_{video_id}.json"
    video_path = f"{VIDEOS_DIR}/video_{video_id}.mp4"
    
    # Limpa vídeos antigos antes de criar novo
    print("🧹 Limpando vídeos antigos...")
    for old_video in os.listdir(VIDEOS_DIR):
        if old_video.endswith('.mp4'):
            old_path = os.path.join(VIDEOS_DIR, old_video)
            os.remove(old_path)
            print(f"🗑️ Removido: {old_video}")
    
    # Sanitiza nomes de arquivos de imagem
    sanitize_image_files()
    
    # Gera legendas
    segments = generate_subtitles(audio_path, subs_path)
    
    # Carrega imagens válidas
    img_files = sorted([
        os.path.join(IMGS_DIR, f) for f in os.listdir(IMGS_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])
    
    if not img_files:
        raise ValueError("❌ Nenhuma imagem encontrada na pasta imagens/")
    
    print(f"🖼️ {len(img_files)} imagens encontradas")
    
    # Calcula duração por imagem
    duration_total = segments[-1][0][1]  # fim do último segmento
    img_duration = duration_total / len(img_files)
    
    # Cria clipes de imagens (formato Reels 9:16)
    img_clips = [
        ImageClip(img, duration=img_duration)
        .resize(height=1920)
        .on_color(size=(1080, 1920), color=(0, 0, 0), pos="center")
        for img in img_files
    ]
    
    # Concatena imagens
    background = concatenate_videoclips(img_clips, method="compose")
    
    # Cria legendas
    text_clips = create_text_clips(segments, width=900)
    
    # Composição final
    final = CompositeVideoClip([background] + text_clips)
    final = final.set_audio(AudioFileClip(audio_path))
    
    # Renderiza
    print("⏳ Renderizando vídeo (pode demorar alguns minutos)...")
    final.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac')
    
    print(f"✅ Vídeo finalizado: {video_path}")
    
    # Limpa arquivos temporários
    if os.path.exists(subs_path):
        os.remove(subs_path)
    
    return video_path

# ========================================
# ROTAS DA API
# ========================================

@app.route("/health")
def health():
    """Verifica se o servidor está funcionando"""
    return jsonify({"status": "ok", "message": "Video Automation Server is running"}), 200

@app.route('/create-video', methods=['POST'])
def create_video_endpoint():
    """
    Endpoint principal: recebe texto e cria vídeo completo
    
    Payload JSON:
    {
        "id": "123",
        "text": "Seu texto aqui"
    }
    
    Retorna:
    {
        "status": "ok",
        "video_file": "/files/video_123.mp4",
        "audio_file": "/files/audio_123.wav"
    }
    """
    try:
        data = request.json
        video_id = data.get("id")
        text = data.get("text")
        
        # Validação
        if not video_id or not text:
            return jsonify({
                "status": "error",
                "message": "Campos obrigatórios: 'id' e 'text'"
            }), 400
        
        print(f"\n{'='*60}")
        print(f"🚀 NOVA REQUISIÇÃO - ID: {video_id}")
        print(f"📝 Texto: {text[:100]}...")
        print(f"{'='*60}\n")
        
        # Verifica se existem imagens
        if not os.path.exists(IMGS_DIR):
            return jsonify({
                "status": "error",
                "message": f"Pasta de imagens não encontrada: {IMGS_DIR}"
            }), 400
        
        img_count = len([f for f in os.listdir(IMGS_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        if img_count == 0:
            return jsonify({
                "status": "error",
                "message": "Nenhuma imagem encontrada na pasta imagens/"
            }), 400
        
        # PROCESSO COMPLETO
        # 1. Gera áudio com gTTS
        audio_path = generate_audio(text, video_id)
        
        # 2. Cria vídeo com legendas
        video_path = create_video(audio_path, video_id)
        
        print(f"\n✅ PROCESSO CONCLUÍDO COM SUCESSO!\n")
        
        return jsonify({
            "status": "ok",
            "video_file": f"/files/videos/video_{video_id}.mp4",
            "audio_file": f"/files/audio_{video_id}.wav",
            "message": "Vídeo criado com sucesso!"
        }), 200
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}\n")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download de arquivos gerados"""
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "Arquivo não encontrado"}), 404

# ========================================
# INICIALIZAÇÃO
# ========================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎬 VIDEO AUTOMATION SERVER (SIMPLE VERSION)")
    print("="*60)
    print(f"📂 Diretório base: {BASE_DIR}")
    print(f"🖼️ Pasta de imagens: {IMGS_DIR}")
    print(f"🎬 Pasta de vídeos: {VIDEOS_DIR}")
    print(f"🎤 Voice sample: {VOICE_SAMPLE}")
    print(f"🔤 Fonte: {FONT_NAME}")
    print("="*60 + "\n")
    
    # Verifica arquivos necessários
    if not os.path.exists(VOICE_SAMPLE):
        print(f"⚠️ ATENÇÃO: Voice sample não encontrado em {VOICE_SAMPLE}")
    
    app.run(host='0.0.0.0', port=5005, debug=False)
