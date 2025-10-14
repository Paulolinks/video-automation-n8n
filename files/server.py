#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Flask para automação de vídeos com TTS
Endpoints:
  - POST /create-audio: Gera áudio com clonagem de voz
  - POST /create-video: Gera vídeo com legendas
  - GET /health: Status do servidor
  - GET /status/<id>: Status de processamento
  - GET /download/audios/<filename>: Baixar áudio
  - GET /download/videos/<filename>: Baixar vídeo
"""

from flask import Flask, request, jsonify, send_file
import subprocess
import os
import threading
import time

# ========================================
# CONFIGURAÇÕES
# ========================================

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_PATH = "/opt/tts-env/bin/python3"
AUDIO_SCRIPT = os.path.join(BASE_DIR, "create_audio.py")
VIDEO_SCRIPT = os.path.join(BASE_DIR, "create_video.py")
AUDIOS_DIR = os.path.join(BASE_DIR, "audios")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
IMGS_DIR = os.path.join(BASE_DIR, "imagens")
VOICE_SAMPLE = os.path.join(BASE_DIR, "voice_sample.wav")

# Controle de processos ativos
active_processes = {}

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def run_audio_creation(audio_id, text):
    """Executa criação de áudio em processo separado"""
    try:
        print(f"\n🎤 Iniciando criação de áudio - ID: {audio_id}")
        print(f"📝 Texto: {text[:100]}...")
        
        # Executa o script de criação de áudio
        result = subprocess.run([
            PYTHON_PATH,
            AUDIO_SCRIPT,
            text,
            audio_id
        ], capture_output=True, text=True, timeout=300)  # 5 minutos timeout
        
        if result.returncode == 0:
            audio_path = os.path.join(AUDIOS_DIR, f"audio_{audio_id}.wav")
            print(f"✅ Áudio {audio_id} criado com sucesso!")
            active_processes[audio_id] = {
                "type": "audio",
                "status": "completed", 
                "message": "Áudio criado com sucesso!",
                "file": audio_path,
                "timestamp": time.time()
            }
        else:
            print(f"❌ Erro na criação do áudio {audio_id}:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            active_processes[audio_id] = {
                "type": "audio",
                "status": "error", 
                "message": result.stderr or result.stdout,
                "timestamp": time.time()
            }
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout na criação do áudio {audio_id}")
        active_processes[audio_id] = {
            "type": "audio",
            "status": "error", 
            "message": "Timeout - áudio demorou mais que 5 minutos",
            "timestamp": time.time()
        }
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        active_processes[audio_id] = {
            "type": "audio",
            "status": "error", 
            "message": str(e),
            "timestamp": time.time()
        }

def run_video_creation(video_id):
    """Executa criação de vídeo em processo separado"""
    try:
        print(f"\n🎬 Iniciando criação de vídeo - ID: {video_id}")
        
        # Executa o script de criação de vídeo
        result = subprocess.run([
            PYTHON_PATH,
            VIDEO_SCRIPT,
            video_id
        ], capture_output=True, text=True, timeout=600)  # 10 minutos timeout
        
        if result.returncode == 0:
            video_path = os.path.join(VIDEOS_DIR, f"video_{video_id}.mp4")
            print(f"✅ Vídeo {video_id} criado com sucesso!")
            active_processes[video_id] = {
                "type": "video",
                "status": "completed", 
                "message": "Vídeo criado com sucesso!",
                "file": video_path,
                "timestamp": time.time()
            }
        else:
            print(f"❌ Erro na criação do vídeo {video_id}:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            active_processes[video_id] = {
                "type": "video",
                "status": "error", 
                "message": result.stderr or result.stdout,
                "timestamp": time.time()
            }
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout na criação do vídeo {video_id}")
        active_processes[video_id] = {
            "type": "video",
            "status": "error", 
            "message": "Timeout - vídeo demorou mais que 10 minutos",
            "timestamp": time.time()
        }
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        active_processes[video_id] = {
            "type": "video",
            "status": "error", 
            "message": str(e),
            "timestamp": time.time()
        }

# ========================================
# ROTAS DA API
# ========================================

@app.route("/health", methods=["GET"])
def health():
    """Verifica se o servidor está funcionando"""
    return jsonify({
        "status": "ok", 
        "message": "Video Automation Server is running",
        "active_processes": len([p for p in active_processes.values() if p.get("status") == "running"])
    }), 200

@app.route('/create-audio', methods=['POST'])
def create_audio_endpoint():
    """
    Endpoint para criar áudio com clonagem de voz
    
    Payload JSON:
    {
        "id": "audio_001",
        "text": "Texto para sintetizar"
    }
    
    Retorna:
    {
        "status": "started",
        "audio_id": "audio_001",
        "message": "Criação de áudio iniciada"
    }
    """
    try:
        data = request.json
        audio_id = data.get("id")
        text = data.get("text")
        
        # Validação
        if not audio_id or not text:
            return jsonify({
                "status": "error",
                "message": "Campos obrigatórios: 'id' e 'text'"
            }), 400
        
        # Verifica se já existe processo para este ID
        if audio_id in active_processes and active_processes[audio_id].get("status") == "running":
            return jsonify({
                "status": "error",
                "message": f"Já existe um processo para o ID {audio_id}"
            }), 400
        
        # Verifica se voice_sample existe
        if not os.path.exists(VOICE_SAMPLE):
            return jsonify({
                "status": "error",
                "message": f"Voice sample não encontrado: {VOICE_SAMPLE}"
            }), 400
        
        # Marca processo como iniciado
        active_processes[audio_id] = {
            "type": "audio",
            "status": "running", 
            "message": "Processando...",
            "timestamp": time.time()
        }
        
        # Inicia criação em thread separada
        thread = threading.Thread(
            target=run_audio_creation,
            args=(audio_id, text),
            daemon=True
        )
        thread.start()
        
        print(f"\n{'='*60}")
        print(f"🚀 NOVA REQUISIÇÃO ÁUDIO - ID: {audio_id}")
        print(f"📝 Texto: {text[:100]}...")
        print(f"{'='*60}\n")
        
        return jsonify({
            "status": "started",
            "audio_id": audio_id,
            "message": "Criação de áudio iniciada com sucesso!",
            "audio_path": f"/audios/audio_{audio_id}.wav"
        }), 200
        
    except Exception as e:
        print(f"\n❌ ERRO NO SERVIDOR: {str(e)}\n")
        return jsonify({
            "status": "error",
            "message": f"Erro no servidor: {str(e)}"
        }), 500

@app.route('/create-video', methods=['POST'])
def create_video_endpoint():
    """
    Endpoint para criar vídeo com legendas
    
    Payload JSON:
    {
        "id": "video_001"
    }
    
    Retorna:
    {
        "status": "started",
        "video_id": "video_001",
        "message": "Criação de vídeo iniciada"
    }
    """
    try:
        data = request.json
        video_id = data.get("id")
        
        # Validação
        if not video_id:
            return jsonify({
                "status": "error",
                "message": "Campo obrigatório: 'id'"
            }), 400
        
        # Verifica se já existe processo para este ID
        if video_id in active_processes and active_processes[video_id].get("status") == "running":
            return jsonify({
                "status": "error",
                "message": f"Já existe um processo para o ID {video_id}"
            }), 400
        
        # Verifica se áudio existe
        audio_path = os.path.join(AUDIOS_DIR, f"audio_{video_id}.wav")
        if not os.path.exists(audio_path):
            return jsonify({
                "status": "error",
                "message": f"Áudio não encontrado: {audio_path}. Crie o áudio primeiro com /create-audio"
            }), 400
        
        # Verifica se existem imagens
        if not os.path.exists(IMGS_DIR):
            return jsonify({
                "status": "error",
                "message": f"Pasta de imagens não encontrada: {IMGS_DIR}"
            }), 400
        
        img_count = len([f for f in os.listdir(IMGS_DIR) 
                        if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        if img_count == 0:
            return jsonify({
                "status": "error",
                "message": "Nenhuma imagem encontrada na pasta imagens/"
            }), 400
        
        # Marca processo como iniciado
        active_processes[video_id] = {
            "type": "video",
            "status": "running", 
            "message": "Processando...",
            "timestamp": time.time()
        }
        
        # Inicia criação em thread separada
        thread = threading.Thread(
            target=run_video_creation,
            args=(video_id,),
            daemon=True
        )
        thread.start()
        
        print(f"\n{'='*60}")
        print(f"🚀 NOVA REQUISIÇÃO VÍDEO - ID: {video_id}")
        print(f"🖼️ Imagens encontradas: {img_count}")
        print(f"{'='*60}\n")
        
        return jsonify({
            "status": "started",
            "video_id": video_id,
            "message": "Criação de vídeo iniciada com sucesso!",
            "images_found": img_count
        }), 200
        
    except Exception as e:
        print(f"\n❌ ERRO NO SERVIDOR: {str(e)}\n")
        return jsonify({
            "status": "error",
            "message": f"Erro no servidor: {str(e)}"
        }), 500

@app.route('/status/<resource_id>', methods=["GET"])
def get_status(resource_id):
    """Verifica status de um áudio ou vídeo específico"""
    if resource_id not in active_processes:
        return jsonify({
            "status": "not_found",
            "message": f"ID {resource_id} não encontrado"
        }), 404
    
    process_data = active_processes[resource_id]
    return jsonify({
        "id": resource_id,
        "type": process_data.get("type"),
        "status": process_data.get("status"),
        "message": process_data.get("message"),
        "file": process_data.get("file")
    }), 200

@app.route('/download/audios/<filename>', methods=["GET"])
def download_audio(filename):
    """Download de arquivos de áudio"""
    file_path = os.path.join(AUDIOS_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "Arquivo não encontrado"}), 404

@app.route('/download/videos/<filename>', methods=["GET"])
def download_video(filename):
    """Download de arquivos de vídeo"""
    file_path = os.path.join(VIDEOS_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "Arquivo não encontrado"}), 404

# ========================================
# LIMPEZA PERIÓDICA
# ========================================

def cleanup_old_processes():
    """Remove processos antigos da memória (completados há mais de 1 hora)"""
    while True:
        time.sleep(300)  # 5 minutos
        current_time = time.time()
        for resource_id in list(active_processes.keys()):
            process = active_processes[resource_id]
            if (process.get("status") in ["completed", "error"] and
                current_time - process.get("timestamp", 0) > 3600):
                del active_processes[resource_id]
                print(f"🧹 Removido processo antigo: {resource_id}")

# ========================================
# INICIALIZAÇÃO
# ========================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌐 VIDEO AUTOMATION SERVER")
    print("="*60)
    print(f"📂 Diretório base: {BASE_DIR}")
    print(f"🐍 Python path: {PYTHON_PATH}")
    print(f"📄 Script de áudio: {AUDIO_SCRIPT}")
    print(f"📄 Script de vídeo: {VIDEO_SCRIPT}")
    print(f"🔗 Endpoints disponíveis:")
    print(f"   - POST /create-audio")
    print(f"   - POST /create-video")
    print(f"   - GET /status/<id>")
    print(f"   - GET /health")
    print(f"   - GET /download/audios/<filename>")
    print(f"   - GET /download/videos/<filename>")
    print("="*60 + "\n")
    
    # Cria diretórios se não existirem
    os.makedirs(AUDIOS_DIR, exist_ok=True)
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    os.makedirs(IMGS_DIR, exist_ok=True)
    
    # Inicia thread de limpeza
    cleanup_thread = threading.Thread(target=cleanup_old_processes, daemon=True)
    cleanup_thread.start()
    
    # Verifica se os scripts existem
    if not os.path.exists(AUDIO_SCRIPT):
        print(f"❌ ERRO: Script de áudio não encontrado: {AUDIO_SCRIPT}")
        exit(1)
    
    if not os.path.exists(VIDEO_SCRIPT):
        print(f"❌ ERRO: Script de vídeo não encontrado: {VIDEO_SCRIPT}")
        exit(1)
    
    # Verifica se o Python existe
    if not os.path.exists(PYTHON_PATH):
        print(f"❌ ERRO: Python não encontrado: {PYTHON_PATH}")
        exit(1)
    
    print("✅ Servidor iniciado com sucesso!")
    app.run(host='0.0.0.0', port=5005, debug=False)
