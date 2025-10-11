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
rm -rf temp_files 2>/dev/null || true
git clone https://github.com/Paulolinks/video-automation-n8n.git temp_files

# Verifica se os arquivos foram baixados
if [ ! -f "temp_files/files/INSTALL_VPS.sh" ]; then
    echo "❌ Erro: INSTALL_VPS.sh não encontrado no GitHub"
    exit 1
fi

# Copia todos os arquivos
cp -r temp_files/files/* /home/n8n/files/
chown -R n8n:n8n /home/n8n/files
rm -rf temp_files

# 2. Executa instalação
echo "⚙️ Executando instalação..."
if [ -f "/home/n8n/files/INSTALL_VPS.sh" ]; then
    chmod +x /home/n8n/files/INSTALL_VPS.sh
    /home/n8n/files/INSTALL_VPS.sh
else
    echo "❌ Erro: INSTALL_VPS.sh não foi copiado corretamente"
    ls -la /home/n8n/files/
    exit 1
fi

echo ""
echo "✅ INSTALAÇÃO CONCLUÍDA!"
echo "🔗 Configure seu N8n para: http://SEU_IP:5005/create-video"
