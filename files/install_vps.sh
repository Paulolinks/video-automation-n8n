#!/bin/bash
# Script de instalação automática para VPS

echo "================================"
echo "🎬 VIDEO AUTOMATION - INSTALLER"
echo "================================"
echo ""

# 1. Atualiza sistema
echo "📦 Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# 2. Instala dependências
echo "📦 Instalando dependências do sistema..."
sudo apt install -y python3-pip python3-venv ffmpeg imagemagick git

# 3. Configura ImageMagick
echo "⚙️ Configurando ImageMagick..."
sudo sed -i 's/<policy domain="path" rights="none" pattern="@\*"\/>/<\!-- <policy domain="path" rights="none" pattern="@\*"\/> -->/' /etc/ImageMagick-6/policy.xml

# 4. Cria diretórios
echo "📁 Criando estrutura de pastas..."
mkdir -p /home/n8n/files/imagens
mkdir -p /home/n8n/files/videos
mkdir -p /home/n8n/files/fonts
mkdir -p /files/imagens
mkdir -p /files/videos
mkdir -p /files/fonts

# Configura permissões para N8n
chown -R n8n:n8n /home/n8n/files
chown -R n8n:n8n /files
chmod 755 /home/n8n/files/imagens
chmod 755 /home/n8n/files/videos
chmod 755 /home/n8n/files/fonts
chmod 755 /files/imagens
chmod 755 /files/videos
chmod 755 /files/fonts

# 5. Cria ambiente virtual
echo "🐍 Criando ambiente virtual Python..."
python3 -m venv /opt/tts-env

# 6. Ativa e instala dependências Python
echo "📦 Instalando dependências Python..."
sudo /opt/tts-env/bin/pip install --upgrade pip

# Tenta instalar dependências com fallback
echo "📦 Instalando dependências principais..."
sudo /opt/tts-env/bin/pip install -r /home/n8n/files/requirements.txt

# Verifica se as dependências foram instaladas
echo "🔍 Verificando instalação das dependências..."
if ! sudo /opt/tts-env/bin/pip list | grep -E "(flask|torch|TTS|moviepy)" > /dev/null; then
    echo "❌ Erro: Dependências não instaladas! Tentando fallback..."
    
    # Fallback: Instala dependências uma por uma
    echo "🔄 Fallback: Instalando dependências individualmente..."
    sudo /opt/tts-env/bin/pip install flask==3.0.0
    sudo /opt/tts-env/bin/pip install torch==2.5.0
    sudo /opt/tts-env/bin/pip install TTS==0.22.0
    sudo /opt/tts-env/bin/pip install moviepy==1.0.3
    sudo /opt/tts-env/bin/pip install whisper-timestamped==1.14.2
    
    # Verifica novamente
    if sudo /opt/tts-env/bin/pip list | grep -E "(flask|torch|TTS|moviepy)" > /dev/null; then
        echo "✅ Fallback: Dependências instaladas com sucesso!"
    else
        echo "❌ Fallback falhou! Instalando versões mais recentes..."
        sudo /opt/tts-env/bin/pip install flask torch TTS moviepy whisper-timestamped
    fi
else
    echo "✅ Dependências instaladas com sucesso!"
fi

# 7. Cria serviço systemd
echo "⚙️ Configurando serviço systemd..."
sudo tee /etc/systemd/system/video-automation.service > /dev/null <<EOF
[Unit]
Description=Video Automation Server
After=network.target

[Service]
Type=simple
User=n8n
Group=n8n
WorkingDirectory=/home/n8n/files
ExecStart=/opt/tts-env/bin/python3 /home/n8n/files/video_automation.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/home/n8n/files
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# 8. Ativa serviço
echo "🚀 Ativando serviço..."
sudo systemctl daemon-reload
sudo systemctl enable video-automation
sudo systemctl start video-automation

# 9. Verifica status
echo ""
echo "✅ Instalação concluída!"
echo ""
echo "📊 Status do serviço:"
sudo systemctl status video-automation --no-pager

# 10. Configura firewall (se necessário)
echo "🔥 Configurando firewall..."
sudo ufw allow 5005/tcp 2>/dev/null || echo "UFW não disponível ou já configurado"

# 11. Verifica se tudo está funcionando
echo "🔍 Verificando instalação..."
if [ -f "/home/n8n/files/video_automation.py" ]; then
    echo "✅ Arquivo principal encontrado"
else
    echo "❌ Arquivo principal não encontrado"
fi

if [ -d "/home/n8n/files/imagens" ] && [ -d "/home/n8n/files/videos" ]; then
    echo "✅ Pastas criadas com sucesso"
else
    echo "❌ Erro ao criar pastas"
fi

# 12. Testa se o servidor Python funciona
echo "🧪 Testando servidor Python..."
if sudo -u n8n timeout 10 /opt/tts-env/bin/python3 /home/n8n/files/video_automation.py &>/dev/null; then
    echo "✅ Servidor Python funciona!"
else
    echo "❌ Erro no servidor Python! Verificando dependências..."
    sudo /opt/tts-env/bin/pip list | grep -E "(flask|torch|TTS|moviepy)" || echo "❌ Dependências em falta!"
fi

echo ""
echo "================================"
echo "🔗 PRÓXIMOS PASSOS:"
echo "================================"
echo "1. Copie voice_sample.wav para /home/n8n/files/"
echo "2. Copie fontes para /home/n8n/files/fonts/"
echo "3. Configure seu N8n para usar:"
echo "   POST http://SEU_IP:5005/create-video"
echo ""
echo "📋 Comandos úteis:"
echo "  Ver logs: sudo journalctl -u video-automation -f"
echo "  Reiniciar: sudo systemctl restart video-automation"
echo "  Parar: sudo systemctl stop video-automation"
echo "  Status: sudo systemctl status video-automation"
echo ""
echo "📂 Estrutura de pastas:"
echo "  /home/n8n/files/imagens/  <- Coloque as imagens aqui"
echo "  /home/n8n/files/videos/   <- Vídeos serão salvos aqui"
echo "  /home/n8n/files/fonts/    <- Fontes para legendas"
echo "================================"

