#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar áudio com clonagem de voz usando TTS (XTTS_v2)
Uso: python3 create_audio.py "<texto>" "<audio_id>"
"""

import sys
import os
from TTS.api import TTS

# ========================================
# CONFIGURAÇÕES
# ========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIOS_DIR = os.path.join(BASE_DIR, "audios")
VOICE_SAMPLE = os.path.join(BASE_DIR, "voice_sample.wav")

# Garante que a pasta audios existe
os.makedirs(AUDIOS_DIR, exist_ok=True)

# ========================================
# FUNÇÃO PRINCIPAL
# ========================================

def generate_audio(text, audio_id):
    """
    Gera áudio com clonagem de voz usando XTTS_v2
    
    Args:
        text: Texto para sintetizar
        audio_id: ID único para o áudio
    
    Returns:
        Path do arquivo de áudio gerado
    """
    output_path = os.path.join(AUDIOS_DIR, f"audio_{audio_id}.wav")
    
    print(f"\n{'='*60}")
    print(f"🎤 GERAÇÃO DE ÁUDIO - ID: {audio_id}")
    print(f"📝 Texto: {text[:100]}...")
    print(f"{'='*60}\n")
    
    # Verifica se voice_sample existe
    if not os.path.exists(VOICE_SAMPLE):
        raise FileNotFoundError(f"❌ Voice sample não encontrado: {VOICE_SAMPLE}")
    
    print(f"🎯 Usando voice sample: {VOICE_SAMPLE}")
    print(f"💾 Áudio será salvo em: {output_path}")
    
    try:
        # Sanitizar texto - remove pontuação que o TTS pode falar
        import re
        text_clean = re.sub(r'[.!?;:]', '', text)  # Remove pontos, exclamação, interrogação, etc
        text_clean = re.sub(r'\s+', ' ', text_clean).strip()  # Remove espaços extras
        
        print(f"📝 Texto original: {text[:50]}...")
        print(f"📝 Texto limpo: {text_clean[:50]}...")
        
        # Inicializa TTS com modelo XTTS_v2 (melhor qualidade de clonagem)
        print("🔄 Carregando modelo XTTS_v2...")
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        
        # Gera áudio clonando a voz do voice_sample
        print("🎙️ Gerando áudio com clonagem de voz...")
        tts.tts_to_file(
            text=text_clean,  # <-- texto limpo
            speaker_wav=VOICE_SAMPLE,
            language="pt",
            file_path=output_path,
            split_sentences=True  # Melhora naturalidade
        )
        
        print(f"\n{'='*60}")
        print(f"✅ ÁUDIO CRIADO COM SUCESSO!")
        print(f"📁 Arquivo: {output_path}")
        print(f"📊 Tamanho: {os.path.getsize(output_path) / 1024:.2f} KB")
        print(f"{'='*60}\n")
        
        return output_path
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ ERRO NA GERAÇÃO DE ÁUDIO: {str(e)}")
        print(f"{'='*60}\n")
        raise

# ========================================
# EXECUÇÃO
# ========================================

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("❌ Uso: python3 create_audio.py \"<texto>\" \"<audio_id>\"")
        print("\nExemplo:")
        print("  python3 create_audio.py \"Olá, este é um teste\" \"teste_001\"")
        sys.exit(1)
    
    text = sys.argv[1]
    audio_id = sys.argv[2]
    
    try:
        generate_audio(text, audio_id)
        sys.exit(0)
    except Exception as e:
        print(f"❌ Falha na execução: {str(e)}")
        sys.exit(1)

