#!/bin/bash
# Script para corrigir dependências Python

echo "🔧 CORRIGINDO DEPENDÊNCIAS PYTHON..."
echo ""

# Verifica se o ambiente virtual existe
if [ ! -d "/opt/tts-env" ]; then
    echo "❌ Ambiente virtual não encontrado! Criando..."
    sudo python3 -m venv /opt/tts-env
fi

# Atualiza pip
echo "📦 Atualizando pip..."
sudo /opt/tts-env/bin/pip install --upgrade pip

# Tenta instalar dependências
echo "📦 Instalando dependências..."
sudo /opt/tts-env/bin/pip install flask==3.0.0
sudo /opt/tts-env/bin/pip install torch==2.5.0
sudo /opt/tts-env/bin/pip install TTS==0.22.0
sudo /opt/tts-env/bin/pip install moviepy==1.0.3
sudo /opt/tts-env/bin/pip install whisper-timestamped==1.14.2

# Verifica se funcionou
echo "🔍 Verificando instalação..."
if sudo /opt/tts-env/bin/pip list | grep -E "(flask|torch|TTS|moviepy)" > /dev/null; then
    echo "✅ Dependências instaladas com sucesso!"
    
    # Testa o servidor
    echo "🧪 Testando servidor..."
    if sudo -u n8n timeout 5 /opt/tts-env/bin/python3 /home/n8n/files/video_automation.py &>/dev/null; then
        echo "✅ Servidor funciona!"
        
        # Reinicia o serviço
        echo "🔄 Reiniciando serviço..."
        sudo systemctl restart video-automation
        sudo systemctl status video-automation --no-pager
    else
        echo "❌ Servidor ainda com problemas"
    fi
else
    echo "❌ Falha na instalação das dependências"
    echo "🔄 Tentando com versões mais recentes..."
    sudo /opt/tts-env/bin/pip install flask torch TTS moviepy whisper-timestamped
fi

echo ""
echo "✅ CORREÇÃO CONCLUÍDA!"
