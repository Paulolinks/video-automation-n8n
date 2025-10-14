#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar vídeo com legendas a partir de áudio e imagens
Uso: python3 create_video.py "<video_id>"
"""

import sys
import os
import json
from moviepy.editor import *
import whisper_timestamped as whisper

# ========================================
# CONFIGURAÇÕES
# ========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIOS_DIR = os.path.join(BASE_DIR, "audios")
IMGS_DIR = os.path.join(BASE_DIR, "imagens")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")

# Configurações de vídeo (formato Reels 9:16)
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 24

# Configurações de legenda
FONT_NAME = "Anton"
FONT_SIZE = 72
FONT_COLOR = "yellow"
STROKE_COLOR = "black"
STROKE_WIDTH = 2

# Garante que pastas existem
os.makedirs(VIDEOS_DIR, exist_ok=True)

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def sanitize_image_files():
    """
    Remove quebras de linha, espaços e caracteres inválidos dos nomes de arquivos.
    Corrige problemas de arquivos salvos pelo N8n com \n no nome.
    """
    if not os.path.exists(IMGS_DIR):
        return
    
    print("🧹 Limpando nomes de arquivos de imagens...")
    
    for fname in os.listdir(IMGS_DIR):
        if not os.path.isfile(os.path.join(IMGS_DIR, fname)):
            continue
        
        # Remove quebras de linha, \r, aspas simples e espaços extras
        clean = fname.replace('\n', '').replace('\r', '').replace("'", "").strip()
        
        old_path = os.path.join(IMGS_DIR, fname)
        new_path = os.path.join(IMGS_DIR, clean)
        
        # Remove arquivos vazios
        if os.path.getsize(old_path) == 0:
            os.remove(old_path)
            print(f"   🗑️ Removido arquivo vazio: {fname}")
            continue
        
        # Renomeia se o nome mudou
        if old_path != new_path and clean:
            try:
                os.rename(old_path, new_path)
                print(f"   🔄 Renomeado: {fname} -> {clean}")
            except Exception as e:
                print(f"   ⚠️ Erro ao renomear {fname}: {e}")
    
    print("✅ Limpeza de nomes concluída")

def generate_subtitles(audio_path):
    """
    Gera legendas com timestamps usando Whisper
    
    Args:
        audio_path: Path do arquivo de áudio
    
    Returns:
        Lista de segmentos [(start, end), texto]
    """
    print("📝 Gerando legendas com Whisper...")
    
    try:
        # Carrega modelo Whisper
        print("🔄 Carregando modelo Whisper...")
        model = whisper.load_model("base")
        
        # Transcreve com timestamps
        print("🎙️ Transcrevendo áudio...")
        result = whisper.transcribe(model, audio_path, language="pt")
        
        # Formata segmentos para o vídeo
        segments = []
        for segment in result['segments']:
            start = segment['start']
            end = segment['end']
            text = segment['text'].strip()
            if text:
                segments.append(((start, end), text))
        
        print(f"✅ {len(segments)} segmentos de legenda criados")
        return segments
        
    except Exception as e:
        print(f"⚠️ Erro na geração de legendas: {str(e)}")
        print("⚠️ Continuando sem legendas...")
        return []

def create_text_clips(segments, width):
    """
    Cria clipes de texto para as legendas
    
    Args:
        segments: Lista de segmentos [(start, end), texto]
        width: Largura do vídeo
    
    Returns:
        Lista de TextClips
    """
    if not segments:
        return []
    
    print(f"📝 Criando {len(segments)} clipes de texto...")
    
    clips = []
    for i, ((start, end), txt) in enumerate(segments):
        try:
            # Cria clipe de texto
            txt_clip = TextClip(
                txt, 
                fontsize=FONT_SIZE, 
                color=FONT_COLOR, 
                font=FONT_NAME,
                size=(width * 0.9, None),  # 90% da largura
                method="caption", 
                align="center",
                stroke_color=STROKE_COLOR,
                stroke_width=STROKE_WIDTH
            ).set_position(("center", "bottom")).set_start(start).set_duration(end - start)
            
            clips.append(txt_clip)
            print(f"   ✓ Clipe {i+1}/{len(segments)}: '{txt[:30]}...'")
            
        except Exception as e:
            print(f"   ⚠️ Erro no clipe {i+1}: {str(e)}")
            continue
    
    print(f"✅ {len(clips)} clipes de texto criados")
    return clips

def create_video(video_id):
    """
    Cria vídeo completo com imagens, áudio e legendas
    
    Args:
        video_id: ID único do vídeo
    
    Returns:
        Path do vídeo gerado
    """
    print(f"\n{'='*60}")
    print(f"🎬 CRIAÇÃO DE VÍDEO - ID: {video_id}")
    print(f"{'='*60}\n")
    
    # Paths
    audio_path = os.path.join(AUDIOS_DIR, f"audio_{video_id}.wav")
    video_path = os.path.join(VIDEOS_DIR, f"video_{video_id}.mp4")
    
    # Verifica se áudio existe
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"❌ Áudio não encontrado: {audio_path}")
    
    print(f"🎵 Áudio encontrado: {audio_path}")
    
    # Verifica se existem imagens
    if not os.path.exists(IMGS_DIR):
        raise FileNotFoundError(f"❌ Pasta de imagens não encontrada: {IMGS_DIR}")
    
    # Sanitiza nomes de arquivos de imagem
    sanitize_image_files()
    
    # Carrega imagens válidas
    img_files = sorted([
        os.path.join(IMGS_DIR, f) for f in os.listdir(IMGS_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])
    
    if not img_files:
        raise ValueError("❌ Nenhuma imagem encontrada na pasta imagens/")
    
    print(f"🖼️ {len(img_files)} imagens encontradas")
    
    # Limpa vídeos antigos antes de criar novo
    print("🧹 Limpando vídeos antigos...")
    for old_video in os.listdir(VIDEOS_DIR):
        if old_video.endswith('.mp4'):
            old_path = os.path.join(VIDEOS_DIR, old_video)
            try:
                os.remove(old_path)
                print(f"   🗑️ Removido: {old_video}")
            except Exception as e:
                print(f"   ⚠️ Erro ao remover {old_video}: {e}")
    
    # Gera legendas (pode falhar, continuará sem legendas)
    segments = generate_subtitles(audio_path)
    
    # Calcula duração por imagem baseado no áudio
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration
    img_duration = audio_duration / len(img_files)
    
    print(f"⏱️ Duração do áudio: {audio_duration:.2f}s")
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
            print(f"   ⚠️ Erro na imagem {i+1}: {str(e)}")
            continue
    
    if not img_clips:
        raise ValueError("❌ Nenhuma imagem foi processada com sucesso")
    
    # Concatena imagens
    print("🔗 Concatenando imagens...")
    background = concatenate_videoclips(img_clips, method="compose")
    
    # Cria legendas
    text_clips = create_text_clips(segments, width=VIDEO_WIDTH)
    
    # Composição final
    print("🎨 Compondo vídeo final...")
    if text_clips:
        final = CompositeVideoClip([background] + text_clips)
    else:
        final = background
    
    final = final.set_audio(audio_clip)
    
    # Renderiza vídeo
    print("⏳ Renderizando vídeo (pode demorar alguns minutos)...")
    final.write_videofile(
        video_path, 
        fps=FPS, 
        codec='libx264', 
        audio_codec='aac',
        verbose=False,
        logger=None
    )
    
    print(f"\n{'='*60}")
    print(f"✅ VÍDEO CRIADO COM SUCESSO!")
    print(f"📁 Arquivo: {video_path}")
    print(f"📊 Tamanho: {os.path.getsize(video_path) / (1024*1024):.2f} MB")
    print(f"{'='*60}\n")
    
    return video_path

# ========================================
# EXECUÇÃO
# ========================================

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("❌ Uso: python3 create_video.py \"<video_id>\"")
        print("\nExemplo:")
        print("  python3 create_video.py \"teste_001\"")
        print("\nNota: O áudio deve estar em audios/audio_<video_id>.wav")
        print("      As imagens devem estar na pasta imagens/")
        sys.exit(1)
    
    video_id = sys.argv[1]
    
    try:
        create_video(video_id)
        sys.exit(0)
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ ERRO: {str(e)}")
        print(f"{'='*60}\n")
        sys.exit(1)
