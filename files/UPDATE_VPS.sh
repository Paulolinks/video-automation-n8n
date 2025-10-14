#!/bin/bash
# ========================================
# ATUALIZAÇÃO RÁPIDA - VIDEO AUTOMATION
# ========================================
# Atualiza apenas os arquivos Python sem reinstalar dependências
# ========================================

set -e

echo "================================"
echo "🔄 VIDEO AUTOMATION - ATUALIZAR"
echo "================================"
echo ""

# Verifica se é root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Execute como root: sudo ./UPDATE_VPS.sh"
    exit 1
fi

# 1. Fazer backup dos arquivos atuais
echo "📦 Fazendo backup dos arquivos atuais..."
cp /home/n8n/files/create_video.py /home/n8n/files/create_video.py.backup 2>/dev/null || true
cp /home/n8n/files/create_audio.py /home/n8n/files/create_audio.py.backup 2>/dev/null || true
cp /home/n8n/files/server.py /home/n8n/files/server.py.backup 2>/dev/null || true

# 2. Baixar arquivos atualizados do GitHub
echo "📥 Baixando arquivos atualizados do GitHub..."
cd /home/n8n
rm -rf temp_update 2>/dev/null || true
git clone --depth 1 https://github.com/Paulolinks/video-automation-n8n.git temp_update

# 3. Copiar arquivos atualizados
echo "📝 Atualizando arquivos Python..."
cp temp_update/files/create_video.py /home/n8n/files/
cp temp_update/files/create_audio.py /home/n8n/files/
cp temp_update/files/server.py /home/n8n/files/
cp temp_update/files/requirements.txt /home/n8n/files/

# 4. Ajustar permissões
echo "🔐 Ajustando permissões..."
chown -R n8n:n8n /home/n8n/files
chmod 644 /home/n8n/files/*.py
chmod 644 /home/n8n/files/requirements.txt

# 5. Limpar pasta temporária
rm -rf temp_update

# 6. Corrigir dependências (Pillow)
echo "📦 Corrigindo dependências..."
sudo -u n8n /opt/tts-env/bin/pip uninstall -y Pillow 2>/dev/null || true
sudo -u n8n /opt/tts-env/bin/pip install Pillow==9.5.0

# 7. Reiniciar serviço
echo "🔄 Reiniciando serviço..."
systemctl restart video-automation

# 8. Aguardar inicialização
sleep 5

# 9. Verificar status
echo ""
echo "================================"
echo "🎉 ATUALIZAÇÃO CONCLUÍDA!"
echo "================================"
echo ""
echo "📊 Status do serviço:"
systemctl status video-automation --no-pager -l | head -15
echo ""

# 10. Testar endpoint
echo "🧪 Testando endpoint..."
if curl -s http://localhost:5005/health | grep -q "ok"; then
    echo "✅ Servidor funcionando corretamente!"
else
    echo "⚠️ Servidor pode estar com problemas. Verifique os logs:"
    echo "   sudo journalctl -u video-automation -n 50"
fi

echo ""
echo "✅ Atualização concluída com sucesso!"
echo ""
echo "💡 Para testar a limpeza de imagens:"
echo "   curl -X POST http://localhost:5005/create-video -H 'Content-Type: application/json' -d '{\"id\": \"teste_update\"}'"
echo ""

