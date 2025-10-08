#!/bin/bash

# 🚀 Script de Instalação para VPS - Sistema de Criação de Vídeos
# Para VPS Hostinger KVM2 (8GB RAM, 2 CPU Cores, 100GB HD)

echo "🚀 Iniciando instalação do sistema de criação de vídeos..."

# 📦 Atualiza sistema
echo "📦 Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# 🐍 Instala Python 3.9+ e dependências
echo "🐍 Instalando Python e dependências..."
sudo apt install -y python3 python3-pip python3-venv ffmpeg imagemagick

# 📁 Cria diretórios necessários
echo "📁 Criando diretórios..."
sudo mkdir -p /home/n8n/files/{imagens,videos,fonts,templates}
sudo chown -R n8n:n8n /home/n8n/files

# 🐍 Cria ambiente virtual Python
echo "🐍 Criando ambiente virtual..."
sudo -u n8n python3 -m venv /opt/tts-env
sudo -u n8n /opt/tts-env/bin/pip install --upgrade pip

# 📚 Instala dependências Python
echo "📚 Instalando dependências Python..."
sudo -u n8n /opt/tts-env/bin/pip install \
    moviepy \
    whisper-timestamped \
    TTS \
    torch \
    torchaudio \
    flask \
    pillow

# 🔧 Instala fontes do sistema
echo "🔧 Instalando fontes..."
sudo cp /home/n8n/files/fonts/*.ttf /usr/share/fonts/truetype/
sudo fc-cache -fv

# 📝 Cria arquivo de configuração
echo "📝 Criando configuração padrão..."
sudo -u n8n cat > /home/n8n/files/config.json << EOF
{
  "default_font": "Anton",
  "default_type": "images",
  "video_quality": "medium",
  "subtitle_size": 72,
  "subtitle_color": "yellow"
}
EOF

# 🔧 Cria serviço systemd para o servidor
echo "🔧 Criando serviço systemd..."
sudo cat > /etc/systemd/system/video-creator.service << EOF
[Unit]
Description=Video Creator API Server
After=network.target

[Service]
Type=simple
User=n8n
WorkingDirectory=/home/n8n/files
ExecStart=/opt/tts-env/bin/python3 /home/n8n/files/server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 🔧 Cria serviço para interface web
sudo cat > /etc/systemd/system/video-web.service << EOF
[Unit]
Description=Video Creator Web Interface
After=network.target

[Service]
Type=simple
User=n8n
WorkingDirectory=/home/n8n/files
ExecStart=/opt/tts-env/bin/python3 /home/n8n/files/web_interface.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 🚀 Inicia serviços
echo "🚀 Iniciando serviços..."
sudo systemctl daemon-reload
sudo systemctl enable video-creator.service
sudo systemctl enable video-web.service
sudo systemctl start video-creator.service
sudo systemctl start video-web.service

# 🔥 Configura firewall
echo "🔥 Configurando firewall..."
sudo ufw allow 5005/tcp  # API Server
sudo ufw allow 5006/tcp  # Web Interface

# 📊 Verifica status
echo "📊 Verificando status dos serviços..."
sudo systemctl status video-creator.service --no-pager
sudo systemctl status video-web.service --no-pager

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "🌐 Acesse a interface web em: http://SEU_IP:5006"
echo "🔗 API disponível em: http://SEU_IP:5005"
echo ""
echo "📋 Endpoints da API:"
echo "  GET  /health - Status do servidor"
echo "  GET  /fonts - Lista fontes disponíveis"
echo "  POST /generate-audio - Gerar áudio"
echo "  POST /generate-video - Gerar vídeo"
echo ""
echo "🔧 Para gerenciar os serviços:"
echo "  sudo systemctl status video-creator"
echo "  sudo systemctl status video-web"
echo "  sudo systemctl restart video-creator"
echo "  sudo systemctl restart video-web"
echo ""
echo "📁 Estrutura de diretórios:"
echo "  /home/n8n/files/imagens/ - Coloque as imagens aqui"
echo "  /home/n8n/files/videos/ - Coloque os vídeos aqui"
echo "  /home/n8n/files/voice_sample.wav - Sua amostra de voz"
echo ""
