#!/bin/bash
# ============================================
# ATUALIZAÇÃO RÁPIDA DO VPS
# ============================================
# Este script atualiza apenas o create_video.py
# sem reinstalar dependências
# ============================================

set -e

echo "============================================"
echo "🔄 ATUALIZAÇÃO RÁPIDA - create_video.py"
echo "============================================"

# Vai para o diretório do projeto
cd /home/n8n/files

# Backup do arquivo atual
echo "📦 Fazendo backup do arquivo atual..."
cp create_video.py create_video.py.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true

# Baixa a versão mais recente do GitHub
echo "⬇️ Baixando versão atualizada do GitHub..."
wget -q https://raw.githubusercontent.com/Paulolinks/video-automation-n8n/master/files/create_video.py -O create_video.py.tmp

# Verifica se o download foi bem-sucedido
if [ $? -eq 0 ] && [ -s create_video.py.tmp ]; then
    echo "✅ Download concluído com sucesso!"
    mv create_video.py.tmp create_video.py
    chmod +x create_video.py
    chown n8n:n8n create_video.py
else
    echo "❌ Erro no download! Mantendo arquivo original."
    rm -f create_video.py.tmp
    exit 1
fi

# Reinicia o serviço
echo "🔄 Reiniciando serviço..."
systemctl restart video-automation

echo ""
echo "============================================"
echo "✅ ATUALIZAÇÃO CONCLUÍDA!"
echo "============================================"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo "1. Teste a criação de vídeo:"
echo "   curl -X POST http://31.97.142.45:5005/create-video \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"id\": \"teste_atualizado\"}'"
echo ""
echo "2. Veja os logs com debug:"
echo "   sudo journalctl -u video-automation -f | grep -E '(DEBUG|ERRO|✓|⚠️)'"
echo ""

