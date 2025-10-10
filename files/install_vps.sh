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
chown -R n8n:n8n /home/n8n/files
chmod 755 /home/n8n/files/imagens
chmod 755 /home/n8n/files/videos
chmod 755 /home/n8n/files/fonts

# 5. Cria ambiente virtual
echo "🐍 Criando ambiente virtual Python..."
python3 -m venv /opt/tts-env

# 6. Ativa e instala dependências Python
echo "📦 Instalando dependências Python..."
source /opt/tts-env/bin/activate
pip install --upgrade pip
pip install -r /home/n8n/files/requirements.txt

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

