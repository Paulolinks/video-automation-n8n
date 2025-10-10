from flask import Flask, render_template, request, jsonify, send_from_directory
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

@app.route('/')
def index():
    return render_template('index.html', fonts=list(AVAILABLE_FONTS.keys()))

@app.route('/api/fonts')
def get_fonts():
    return jsonify({"fonts": list(AVAILABLE_FONTS.keys())})

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    config_file = '/home/n8n/files/config.json'
    
    if request.method == 'GET':
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return jsonify(json.load(f))
        else:
            return jsonify({
                "default_font": "Anton",
                "default_type": "images",
                "video_quality": "medium",
                "subtitle_size": 72,
                "subtitle_color": "yellow"
            })
    
    elif request.method == 'POST':
        data = request.json
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)
        return jsonify({"status": "success"})

if __name__ == '__main__':
    # Cria diretório de templates se não existir
    os.makedirs('templates', exist_ok=True)
    app.run(host='0.0.0.0', port=5006)
