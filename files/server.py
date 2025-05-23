from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/health")
def health():
    return "ok", 200

@app.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.json
    video_id = data.get("id")
    frase = data.get("frase")

    if not video_id or not frase:
        return jsonify({"error": "Missing 'id' or 'frase'"}), 400

    try:
        result = subprocess.run([
            "/opt/tts-env/bin/python3",
            "/home/n8n/files/make_video.py",
            frase,
            str(video_id)
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

