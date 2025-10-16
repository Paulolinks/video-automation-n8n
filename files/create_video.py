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
    
    # Processar imagens
    print("🖼️ Processando...")
    img_clips = []
    
    for i, img_path in enumerate(img_files):
        try:
            img_clip = ImageClip(img_path).set_duration(img_duration).set_fps(FPS)
            img_clip = img_clip.resize(height=VIDEO_HEIGHT)
            img_clip = img_clip.on_color(
                size=(VIDEO_WIDTH, VIDEO_HEIGHT),
                color=(0, 0, 0),
                pos="center"
            ).set_fps(FPS)
            img_clips.append(img_clip)
            print(f"   ✓ {i+1}/{len(img_files)}")
        except Exception as e:
            print(f"   ⚠️ Pulou {i+1}: {e}")
    
    if not img_clips:
        raise ValueError("❌ Nenhuma imagem processada")
    
    # Concatenar
    print("🔗 Concatenando...")
    video = concatenate_videoclips(img_clips, method="compose").set_fps(FPS)
    
    # Adicionar áudio
    print("🎵 Adicionando áudio...")
    video = video.set_audio(audio_clip)
    
    # Renderizar
    print("⏳ Renderizando...")
    video.write_videofile(
        video_path,
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        preset='ultrafast',
        threads=4,
        verbose=False,
        logger=None
    )
    
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
