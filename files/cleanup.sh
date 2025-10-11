#!/bin/bash
# Script para limpar instalação anterior (local errado)

echo "🧹 LIMPANDO INSTALAÇÃO ANTERIOR..."
echo ""

# Para serviços antigos
echo "🛑 Parando serviços antigos..."
sudo systemctl stop video-creator.service 2>/dev/null || echo "Serviço video-creator não encontrado"
sudo systemctl stop video-automation.service 2>/dev/null || echo "Serviço video-automation não encontrado"
sudo systemctl stop video-web.service 2>/dev/null || echo "Serviço video-web não encontrado"

# Remove serviços systemd antigos
echo "🗑️ Removendo serviços systemd antigos..."
sudo rm -f /etc/systemd/system/video-creator.service
sudo rm -f /etc/systemd/system/video-automation.service
sudo rm -f /etc/systemd/system/video-web.service
sudo systemctl daemon-reload

# Remove arquivos da pasta root (instalação errada)
echo "🗑️ Removendo arquivos da pasta root..."
sudo rm -rf /root/video-automation-n8n

# Remove ambiente virtual antigo (se existir)
echo "🗑️ Removendo ambiente virtual antigo..."
sudo rm -rf /opt/tts-env

# Remove Rust do usuário n8n
echo "🗑️ Removendo Rust do usuário n8n..."
sudo rm -rf /home/n8n/.cargo
sudo rm -rf /home/n8n/.rustup

# Remove Rust do root
echo "🗑️ Removendo Rust do root..."
sudo rm -rf /root/.cargo
sudo rm -rf /root/.rustup

# Limpa cache do pip
echo "🗑️ Limpando cache do pip..."
sudo -u n8n rm -rf /home/n8n/.cache/pip 2>/dev/null || true

# Limpa pasta /home/n8n/files (se existir)
echo "🗑️ Limpando pasta /home/n8n/files..."
sudo rm -rf /home/n8n/files/*

echo ""
echo "✅ LIMPEZA CONCLUÍDA!"
echo "🚀 Agora execute o comando de instalação:"
echo "sudo curl -sSL https://raw.githubusercontent.com/Paulolinks/video-automation-n8n/master/files/quick_install.sh | bash"
echo ""
