from flask import Flask, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)

# 📁 Lista de fontes disponíveis
AVAILABLE_FONTS = {
    "Active_Heart": "Active_Heart.ttf",
    "Anton": "anton.ttf", 
    "Bold": "bold.ttf",
    "Loucos": "Loucos.ttf",
    "Loucos2": "Loucos2.ttf",
    "New": "new.ttf",
    "Thequir": "THEQUIR.ttf",
    "Typo": "Typo.ttf",
    "Wallman_Bold": "Wallman-Bold.ttf"
}

@app.route("/health")
def health():
    return "ok", 200

@app.route('/fonts', methods=['GET'])
def get_fonts():
    """Retorna lista de fontes disponíveis"""
    return jsonify({"fonts": list(AVAILABLE_FONTS.keys())})

@app.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.json
    video_id = data.get("id")
    frase = data.get("frase")
    font_name = data.get("font", "Anton")  # Fonte padrão
    video_type = data.get("type", "images")  # "images" ou "videos"
    
    if not video_id or not frase:
        return jsonify({"error": "Missing 'id' or 'frase'"}), 400

    # Valida se a fonte existe
    if font_name not in AVAILABLE_FONTS:
        return jsonify({"error": f"Font '{font_name}' not available"}), 400

    try:
        # Escolhe o script baseado no tipo
        script_name = "make_video.py" if video_type == "images" else "make_video_with_videos.py"
        
        result = subprocess.run([
            "/opt/tts-env/bin/python3",
            f"/home/n8n/files/{script_name}",
            frase,
            str(video_id),
            font_name
        ], capture_output=True, text=True)

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode != 0:
            return jsonify({"status": "error", "message": result.stderr}), 500

        return jsonify({"status": "ok", "file": f"/files/video_{video_id}.mp4"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/generate-audio', methods=['POST'])  # <-- ADICIONE ISSO
def generate_audio():
    data = request.json
    frase = data.get("frase")
    audio_id = data.get("id")
    
    if not frase or not audio_id:
        return jsonify({"error": "Missing 'frase' or 'id'"}), 400

    try:
        result = subprocess.run([
            "/opt/tts-env/bin/python3",
            "/home/n8n/files/tts_audio_highquality.py",
            frase,
            str(audio_id)
        ], capture_output=True, text=True)

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode != 0:
            return jsonify({"status": "error", "message": result.stderr}), 500

        return jsonify({"status": "ok", "file": f"/files/audio_{audio_id}.wav"})
    except subprocess.CalledProcessError:
        return jsonify({"status": "error", "message": "TTS failed"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)

