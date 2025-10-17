#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from moviepy.editor import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIOS_DIR = os.path.join(BASE_DIR, "audios")
IMGS_DIR = os.path.join(BASE_DIR, "imagens")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 24

os.makedirs(VIDEOS_DIR, exist_ok=True)

def sanitize_image_files():
    if not os.path.exists(IMGS_DIR):
        return
    print("🧹 Limpando nomes de arquivos...")
    for fname in os.listdir(IMGS_DIR):
        if not os.path.isfile(os.path.join(IMGS_DIR, fname)):
            continue
        clean = fname.replace('\n', '').replace('\r', '').replace("'", "").strip()
        old_path = os.path.join(IMGS_DIR, fname)
        new_path = os.path.join(IMGS_DIR, clean)
        if os.path.getsize(old_path) == 0:
            os.remove(old_path)
            continue
        if old_path != new_path and clean:
            try:
                os.rename(old_path, new_path)
            except:
                pass
    print("✅ Limpeza concluída")

def create_video(video_id):
    print(f"\n{'='*60}")
    print(f"🎬 VÍDEO - ID: {video_id}")
    print(f"{'='*60}\n")
    
    audio_path = os.path.join(AUDIOS_DIR, f"audio_{video_id}.wav")
    video_path = os.path.join(VIDEOS_DIR, f"video_{video_id}.mp4")
    
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"❌ Áudio não encontrado: {audio_path}")
    
    print(f"🎵 Áudio: {audio_path}")
    
    sanitize_image_files()
    
    img_files = sorted([
        os.path.join(IMGS_DIR, f) for f in os.listdir(IMGS_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])
    
    if not img_files:
        raise ValueError("❌ Nenhuma imagem encontrada")
    
    print(f"🖼️ {len(img_files)} imagens")
    
    # Limpar vídeos antigos
    for old in os.listdir(VIDEOS_DIR):
        if old.endswith('.mp4'):
            try:
                os.remove(os.path.join(VIDEOS_DIR, old))
            except:
                pass
    
    # Calcular durações
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration
    img_duration = audio_duration / len(img_files)
    
    print(f"⏱️ Áudio: {audio_duration:.2f}s | Por imagem: {img_duration:.2f}s")
    
    # Processar imagens - MÉTODO ALTERNATIVO usando ffmpeg diretamente
    print("🖼️ Processando imagens com ffmpeg...")
    
    # Criar arquivo de lista para ffmpeg
    import subprocess
    filelist_path = os.path.join(VIDEOS_DIR, f"filelist_{video_id}.txt")
    
    with open(filelist_path, 'w') as f:
        for img_path in img_files:
            f.write(f"file '{img_path}'\n")
            f.write(f"duration {img_duration}\n")
        # Adiciona última imagem novamente para fechar o loop
        f.write(f"file '{img_files[-1]}'\n")
    
    print(f"⏱️ Cada imagem: {img_duration:.2f}s")
    
    # Renderizar vídeo SEM áudio usando ffmpeg diretamente
    print("⏳ Renderizando vídeo com ffmpeg...")
    temp_video = video_path.replace('.mp4', '_temp.mp4')
    
    # Comando ffmpeg para criar vídeo a partir das imagens
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', filelist_path,
        '-vf', f'scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2,setsar=1',
        '-r', str(FPS),
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-pix_fmt', 'yuv420p',
        temp_video
    ]
    
    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Erro ffmpeg (vídeo): {result.stderr}")
        raise Exception("Falha ao criar vídeo com ffmpeg")
    
    # Limpar arquivo de lista
    try:
        os.remove(filelist_path)
    except:
        pass
    
    # Adicionar áudio usando ffmpeg diretamente
    print("🎵 Adicionando áudio com ffmpeg...")
    result = subprocess.run([
        'ffmpeg', '-i', temp_video, '-i', audio_path,
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
        '-shortest', '-y', video_path
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Erro ffmpeg: {result.stderr}")
        raise Exception("Falha ao adicionar áudio com ffmpeg")
    
    # Limpar arquivo temporário
    try:
        os.remove(temp_video)
    except:
        pass
    
    size_mb = os.path.getsize(video_path) / (1024*1024)
    print(f"\n{'='*60}")
    print(f"✅ VÍDEO CRIADO!")
    print(f"📁 {video_path}")
    print(f"📊 {size_mb:.2f} MB")
    print(f"{'='*60}\n")
    
    return video_path

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("❌ Uso: python3 create_video.py <video_id>")
        sys.exit(1)
    
    try:
        create_video(sys.argv[1])
    except Exception as e:
        print(f"❌ ERRO: {e}")
        sys.exit(1)
