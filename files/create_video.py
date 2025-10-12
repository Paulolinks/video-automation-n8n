import sys
import os
import json
from TTS.api import TTS
from moviepy.editor import *
from whisper_timestamped import load_model, transcribe_timestamped

# ========================================
# CONFIGURAÇÕES
# ========================================

# Diretórios
BASE_DIR = "/home/n8n/files"
IMGS_DIR = os.path.join(BASE_DIR, "imagens")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
VOICE_SAMPLE = os.path.join(BASE_DIR, "voice_sample.wav")
FONT_NAME = "Anton"  # Fonte padrão

# Configurações de vídeo (formato Reels 9:16)
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920

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

def generate_audio_with_voice_cloning(text, audio_id):
    """Gera áudio com clonagem de voz usando TTS"""
    audio_path = f"{BASE_DIR}/audio_{audio_id}.wav"
    
    print(f"🎤 Gerando áudio com clonagem de voz para ID: {audio_id}")
    print(f"🎯 Usando voice sample: {VOICE_SAMPLE}")
    
    try:
        # Inicializa TTS com modelo XTTS_v2 para clonagem
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        
        # Gera áudio clonando a voz do voice_sample
        tts.tts_to_file(
            text=text,
            speaker_wav=VOICE_SAMPLE,
            language="pt",
            file_path=audio_path
        )
        
        print(f"✅ Áudio criado com clonagem de voz: {audio_path}")
        return audio_path
        
    except Exception as e:
        print(f"❌ Erro na geração de áudio: {str(e)}")
        raise

def generate_subtitles(audio_path, subs_path):
    """Gera legendas com timestamps usando Whisper"""
    print("📝 Gerando legendas com Whisper...")
    
    try:
        # Carrega modelo Whisper
        model = load_model("base")
        
        # Transcreve com timestamps
        result = transcribe_timestamped(model, audio_path, language="pt")
        
        # Salva resultado completo
        with open(subs_path, "w", encoding="utf-8") as f:
            json.dump(result["segments"], f, ensure_ascii=False, indent=2)
        
        # Formata segmentos para o vídeo
        segments = [((seg["start"], seg["end"]), seg["text"]) for seg in result["segments"]]
        print(f"✅ {len(segments)} segmentos de legenda criados")
        return segments
        
    except Exception as e:
        print(f"❌ Erro na geração de legendas: {str(e)}")
        raise

def create_text_clips(segments, width):
    """Cria clipes de texto para as legendas"""
    print(f"📝 Criando {len(segments)} clipes de texto...")
    
    clips = []
    for i, ((start, end), txt) in enumerate(segments):
        try:
            # Cria clipe de texto
            txt_clip = TextClip(
                txt, 
                fontsize=72, 
                color="yellow", 
                font=FONT_NAME,
                size=(width, None), 
                method="caption", 
                align="center",
                stroke_color="black",
                stroke_width=2
            ).set_position("center").set_start(start).set_end(end)
            
            clips.append(txt_clip)
            print(f"   ✓ Clipe {i+1}/{len(segments)}: '{txt[:30]}...'")
            
        except Exception as e:
            print(f"   ❌ Erro no clipe {i+1}: {str(e)}")
            continue
    
    print(f"✅ {len(clips)} clipes de texto criados")
    return clips

def create_video_composition(audio_path, video_id):
    """Cria vídeo completo com imagens, áudio e legendas"""
    print("🎬 Iniciando criação do vídeo...")
    
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
    
    # Gera legendas (DESABILITADO - Whisper trava o processo)
    # segments = generate_subtitles(audio_path, subs_path)
    segments = []  # Sem legendas por enquanto
    print("⚠️ Legendas desabilitadas temporariamente (Whisper causa timeout)")
    
    # Carrega imagens válidas
    img_files = sorted([
        os.path.join(IMGS_DIR, f) for f in os.listdir(IMGS_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])
    
    if not img_files:
        raise ValueError("❌ Nenhuma imagem encontrada na pasta imagens/")
    
    print(f"🖼️ {len(img_files)} imagens encontradas")
    
    # Calcula duração por imagem baseado no áudio
    audio_duration = AudioFileClip(audio_path).duration
    img_duration = audio_duration / len(img_files)
    
    print(f"🎵 Duração do áudio: {audio_duration:.2f}s")
    print(f"⏱️ Duração por imagem: {img_duration:.2f}s")
    
    # Cria clipes de imagens (formato Reels 9:16)
    print("🖼️ Processando imagens...")
    img_clips = []
    for i, img_path in enumerate(img_files):
        try:
            # Carrega imagem e redimensiona para formato Reels
            img_clip = ImageClip(img_path, duration=img_duration)
            img_clip = img_clip.resize(height=VIDEO_HEIGHT)
            
            # Centraliza em fundo preto
            img_clip = img_clip.on_color(
                size=(VIDEO_WIDTH, VIDEO_HEIGHT), 
                color=(0, 0, 0), 
                pos="center"
            )
            
            img_clips.append(img_clip)
            print(f"   ✓ Imagem {i+1}/{len(img_files)}: {os.path.basename(img_path)}")
            
        except Exception as e:
            print(f"   ❌ Erro na imagem {i+1}: {str(e)}")
            continue
    
    if not img_clips:
        raise ValueError("❌ Nenhuma imagem foi processada com sucesso")
    
    # Concatena imagens
    print("🔗 Concatenando imagens...")
    background = concatenate_videoclips(img_clips, method="compose")
    
    # Cria legendas
    text_clips = create_text_clips(segments, width=900)
    
    # Composição final
    print("🎨 Compondo vídeo final...")
    final = CompositeVideoClip([background] + text_clips)
    final = final.set_audio(AudioFileClip(audio_path))
    
    # Renderiza vídeo
    print("⏳ Renderizando vídeo (pode demorar alguns minutos)...")
    final.write_videofile(
        video_path, 
        fps=24, 
        codec='libx264', 
        audio_codec='aac',
        verbose=False,
        logger=None
    )
    
    print(f"✅ Vídeo finalizado: {video_path}")
    
    # Limpa arquivos temporários
    if os.path.exists(subs_path):
        os.remove(subs_path)
        print("🗑️ Arquivo de legendas temporário removido")
    
    return video_path

# ========================================
# FUNÇÃO PRINCIPAL
# ========================================

def main():
    """Função principal que processa argumentos da linha de comando"""
    if len(sys.argv) != 3:
        print("❌ Uso: python create_video.py <texto> <video_id>")
        sys.exit(1)
    
    text = sys.argv[1]
    video_id = sys.argv[2]
    
    print(f"\n{'='*60}")
    print(f"🎬 CRIAÇÃO DE VÍDEO - ID: {video_id}")
    print(f"📝 Texto: {text[:100]}...")
    print(f"{'='*60}\n")
    
    try:
        # 1. Gera áudio com clonagem de voz
        audio_path = generate_audio_with_voice_cloning(text, video_id)
        
        # 2. Cria vídeo completo
        video_path = create_video_composition(audio_path, video_id)
        
        # 3. Limpa arquivo de áudio temporário
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print("🗑️ Arquivo de áudio temporário removido")
        
        print(f"\n{'='*60}")
        print(f"🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
        print(f"📁 Vídeo salvo em: {video_path}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ ERRO: {str(e)}")
        print(f"{'='*60}\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
