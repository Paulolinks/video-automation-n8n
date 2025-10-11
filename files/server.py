from flask import Flask, request, jsonify
import subprocess
import os
import threading
import time

# ========================================
# CONFIGURAÇÕES
# ========================================
app = Flask(__name__)

# Diretórios
BASE_DIR = "/home/n8n/files"
PYTHON_PATH = "/opt/tts-env/bin/python3"
PROCESSOR_SCRIPT = os.path.join(BASE_DIR, "create_video.py")

# Controle de execução
active_processes = {}

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def run_video_creation(video_id, text):
    """Executa criação de vídeo em processo separado"""
    try:
        print(f"\n🎬 Iniciando criação de vídeo - ID: {video_id}")
        print(f"📝 Texto: {text[:100]}...")
        
        # Executa o script de criação de vídeo
        result = subprocess.run([
            PYTHON_PATH,
            PROCESSOR_SCRIPT,
            text,
            video_id
        ], capture_output=True, text=True, timeout=600)  # 10 minutos timeout
        
        if result.returncode == 0:
            print(f"✅ Vídeo {video_id} criado com sucesso!")
            active_processes[video_id] = {"status": "completed", "message": "Vídeo criado com sucesso!"}
        else:
            print(f"❌ Erro na criação do vídeo {video_id}:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            active_processes[video_id] = {"status": "error", "message": result.stderr}
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout na criação do vídeo {video_id}")
        active_processes[video_id] = {"status": "error", "message": "Timeout - vídeo demorou mais que 10 minutos"}
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        active_processes[video_id] = {"status": "error", "message": str(e)}

# ========================================
# ROTAS DA API
# ========================================

@app.route("/health")
def health():
    """Verifica se o servidor está funcionando"""
    return jsonify({
        "status": "ok", 
        "message": "Video Automation Server is running",
        "active_processes": len([p for p in active_processes.values() if p.get("status") == "running"])
    }), 200

@app.route('/create-video', methods=['POST'])
def create_video_endpoint():
    """
    Endpoint principal: recebe texto e inicia criação de vídeo
    
    Payload JSON:
    {
        "id": "123",
        "text": "Seu texto aqui"
    }
    
    Retorna:
    {
        "status": "started",
        "video_id": "123",
        "message": "Criação de vídeo iniciada"
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
        
        # Verifica se já existe processo para este ID
        if video_id in active_processes:
            return jsonify({
                "status": "error",
                "message": f"Já existe um processo para o ID {video_id}"
            }), 400
        
        # Verifica se existem imagens
        imgs_dir = os.path.join(BASE_DIR, "imagens")
        if not os.path.exists(imgs_dir):
            return jsonify({
                "status": "error",
                "message": f"Pasta de imagens não encontrada: {imgs_dir}"
            }), 400
        
        img_count = len([f for f in os.listdir(imgs_dir) 
                        if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        if img_count == 0:
            return jsonify({
                "status": "error",
                "message": "Nenhuma imagem encontrada na pasta imagens/"
            }), 400
        
        # Marca processo como iniciado
        active_processes[video_id] = {"status": "running", "message": "Processando..."}
        
        # Inicia criação em thread separada
        thread = threading.Thread(
            target=run_video_creation,
            args=(video_id, text),
            daemon=True
        )
        thread.start()
        
        print(f"\n{'='*60}")
        print(f"🚀 NOVA REQUISIÇÃO - ID: {video_id}")
        print(f"📝 Texto: {text[:100]}...")
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

@app.route('/status/<video_id>')
def get_status(video_id):
    """Verifica status de um vídeo específico"""
    if video_id not in active_processes:
        return jsonify({
            "status": "not_found",
            "message": f"ID {video_id} não encontrado"
        }), 404
    
    return jsonify({
        "video_id": video_id,
        "status": active_processes[video_id]["status"],
        "message": active_processes[video_id]["message"]
    }), 200

@app.route('/download/<filename>')
def download_file(filename):
    """Download de arquivos gerados"""
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "Arquivo não encontrado"}), 404

# ========================================
# LIMPEZA PERIÓDICA
# ========================================

def cleanup_old_processes():
    """Remove processos antigos da memória"""
    while True:
        time.sleep(300)  # 5 minutos
        # Remove processos completados há mais de 1 hora
        current_time = time.time()
        for video_id in list(active_processes.keys()):
            if (active_processes[video_id].get("status") in ["completed", "error"] and
                current_time - active_processes[video_id].get("timestamp", 0) > 3600):
                del active_processes[video_id]

# ========================================
# INICIALIZAÇÃO
# ========================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌐 VIDEO AUTOMATION SERVER")
    print("="*60)
    print(f"📂 Diretório base: {BASE_DIR}")
    print(f"🐍 Python path: {PYTHON_PATH}")
    print(f"📄 Script processador: {PROCESSOR_SCRIPT}")
    print(f"🔗 Endpoints disponíveis:")
    print(f"   - POST /create-video")
    print(f"   - GET /status/<video_id>")
    print(f"   - GET /health")
    print(f"   - GET /download/<filename>")
    print("="*60 + "\n")
    
    # Inicia thread de limpeza
    cleanup_thread = threading.Thread(target=cleanup_old_processes, daemon=True)
    cleanup_thread.start()
    
    # Verifica se o script processador existe
    if not os.path.exists(PROCESSOR_SCRIPT):
        print(f"❌ ERRO: Script processador não encontrado: {PROCESSOR_SCRIPT}")
        exit(1)
    
    # Verifica se o Python existe
    if not os.path.exists(PYTHON_PATH):
        print(f"❌ ERRO: Python não encontrado: {PYTHON_PATH}")
        exit(1)
    
    print("✅ Servidor iniciado com sucesso!")
    app.run(host='0.0.0.0', port=5005, debug=False)
