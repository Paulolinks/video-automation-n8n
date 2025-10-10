#!/bin/bash
# Script de instalação rápida - apenas 2 comandos!

echo "================================"
echo "🚀 VIDEO AUTOMATION - INSTALLER"
echo "================================"
echo ""

# Verifica se é root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Execute como root: sudo ./quick_install.sh"
    exit 1
fi

# 1. Baixa arquivos do GitHub
echo "📥 Baixando arquivos do GitHub..."
cd /home/n8n
git clone https://github.com/Paulolinks/video-automation-n8n.git temp_files
cp -r temp_files/files/* /home/n8n/files/
chown -R n8n:n8n /home/n8n/files
rm -rf temp_files

# 2. Executa instalação
echo "⚙️ Executando instalação..."
chmod +x /home/n8n/files/INSTALL_VPS.sh
/home/n8n/files/INSTALL_VPS.sh

echo ""
echo "✅ INSTALAÇÃO CONCLUÍDA!"
echo "🔗 Configure seu N8n para: http://SEU_IP:5005/create-video"
