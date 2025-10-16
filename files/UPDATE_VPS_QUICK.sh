#!/bin/bash
# Script de atualização rápida do VPS
# Uso: curl -sSL https://raw.githubusercontent.com/Paulolinks/video-automation-n8n/master/files/UPDATE_VPS_QUICK.sh | sudo bash

echo "🔄 ATUALIZAÇÃO RÁPIDA DO VPS"
echo "============================================================"

# Parar serviço
echo "⏸️ Parando serviço..."
systemctl stop video-automation

# Baixar arquivos atualizados
echo "📥 Baixando arquivos do GitHub..."
cd /home/n8n/files

# Backup dos arquivos antigos
echo "💾 Fazendo backup..."
cp create_video.py create_video.py.bak 2>/dev/null
cp create_audio.py create_audio.py.bak 2>/dev/null
cp server.py server.py.bak 2>/dev/null

# Baixar novos arquivos
echo "⬇️ Baixando create_video.py..."
sudo -u n8n curl -o create_video.py https://raw.githubusercontent.com/Paulolinks/video-automation-n8n/master/files/create_video.py

echo "⬇️ Baixando create_audio.py..."
sudo -u n8n curl -o create_audio.py https://raw.githubusercontent.com/Paulolinks/video-automation-n8n/master/files/create_audio.py

echo "⬇️ Baixando server.py..."
sudo -u n8n curl -o server.py https://raw.githubusercontent.com/Paulolinks/video-automation-n8n/master/files/server.py

# Ajustar permissões
echo "🔐 Ajustando permissões..."
chmod +x /home/n8n/files/*.py
chown -R n8n:n8n /home/n8n/files/

# Reiniciar serviço
echo "🚀 Reiniciando serviço..."
systemctl start video-automation

# Aguardar inicialização
sleep 5

# Verificar status
echo ""
echo "✅ STATUS DO SERVIÇO:"
systemctl status video-automation --no-pager -l

echo ""
echo "🧪 TESTANDO SERVIDOR:"
curl -s http://localhost:5005/health | head -20

echo ""
echo "============================================================"
echo "✅ ATUALIZAÇÃO CONCLUÍDA!"
echo ""
echo "📝 COMANDOS ÚTEIS:"
echo "  - Ver logs: sudo journalctl -u video-automation -f"
echo "  - Testar: curl http://localhost:5005/health"
echo "  - Parar: sudo systemctl stop video-automation"
echo "  - Iniciar: sudo systemctl start video-automation"
echo "============================================================"
