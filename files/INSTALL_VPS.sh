#!/bin/bash
# ========================================
# INSTALAÇÃO AUTOMÁTICA - VIDEO AUTOMATION
# ========================================
# Este script faz TUDO automaticamente:
# - Detecta e instala Python 3.11
# - Instala todas as dependências
# - Configura permissões
# - Cria serviço systemd
# - Testa funcionamento
# ========================================

set -e  # Para na primeira falha
trap 'echo "❌ ERRO na linha $LINENO"; exit 1' ERR

echo "================================"
echo "🎬 VIDEO AUTOMATION - INSTALLER"
echo "================================"
echo ""

# Verifica se é root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Execute como root: sudo ./INSTALL_VPS.sh"
    exit 1
fi

# 1. Atualiza sistema
echo "🔄 Atualizando sistema..."
apt update -y
apt upgrade -y

# 2. Instala Python 3.11 se necessário
echo "🐍 Verificando Python 3.11..."
if ! command -v python3.11 >/dev/null 2>&1; then
    echo "📥 Python 3.11 não encontrado, instalando via PPA deadsnakes..."
    
    # Adicionar repositório deadsnakes
    apt install -y software-properties-common
    add-apt-repository ppa:deadsnakes/ppa -y
    apt update
    
    # Instalar Python 3.11 (pip é independente)
    apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
    
    if ! command -v python3.11 >/dev/null 2>&1; then
        echo "❌ ERRO CRÍTICO: Falha ao instalar Python 3.11"
        exit 1
    fi
else
    echo "✅ Python 3.11 já instalado"
fi

echo "✅ Python 3.11: $(python3.11 --version)"

# 3. Instala dependências do sistema
echo "📦 Instalando dependências do sistema..."
apt install -y ffmpeg espeak-ng
apt install -y curl wget git build-essential
apt install -y libsndfile1 libsndfile1-dev
apt install -y portaudio19-dev

# 4. Cria usuário n8n se não existir
echo "👤 Configurando usuário n8n..."
if ! id "n8n" &>/dev/null; then
    useradd -m -s /bin/bash n8n
    echo "✅ Usuário n8n criado"
else
    echo "✅ Usuário n8n já existe"
fi

# 5. Cria diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p /home/n8n/files/imagens
mkdir -p /home/n8n/files/videos
mkdir -p /home/n8n/files/fonts
mkdir -p /files/imagens
mkdir -p /files/videos
mkdir -p /files/fonts

# 6. Configura permissões
echo "🔐 Configurando permissões..."
chown -R n8n:n8n /home/n8n/files
chown -R n8n:n8n /files
chmod 755 /home/n8n/files/imagens
chmod 755 /home/n8n/files/videos
chmod 755 /home/n8n/files/fonts
chmod 755 /files/imagens
chmod 755 /files/videos
chmod 755 /files/fonts

# 7. Cria ambiente virtual com Python 3.11 FORÇADO
echo "🐍 Criando ambiente virtual Python 3.11..."
rm -rf /opt/tts-env
python3.11 -m venv /opt/tts-env
chown -R n8n:n8n /opt/tts-env

# Verifica versão dentro do venv
VENV_PYTHON_VERSION=$(/opt/tts-env/bin/python3 --version)
echo "✅ Ambiente virtual: $VENV_PYTHON_VERSION"

if [[ ! "$VENV_PYTHON_VERSION" =~ "3.11" ]]; then
    echo "❌ ERRO: Ambiente virtual não está usando Python 3.11"
    exit 1
fi

# 8. Atualiza pip
echo "📦 Atualizando pip..."
sudo -u n8n /opt/tts-env/bin/pip install --upgrade pip

# 9. Instala dependências Python NA ORDEM CORRETA
echo "📦 Instalando dependências Python com versões compatíveis..."

echo "   - Flask..."
sudo -u n8n /opt/tts-env/bin/pip install flask==3.0.0

echo "   - PyTorch..."
sudo -u n8n /opt/tts-env/bin/pip install torch==2.5.0

echo "   - Tokenizers (versão pré-compilada)..."
sudo -u n8n /opt/tts-env/bin/pip install tokenizers==0.12.1

echo "   - Transformers (compatível com tokenizers 0.12.1)..."
sudo -u n8n /opt/tts-env/bin/pip install transformers==4.20.1

echo "   - Instalando dependências do TTS..."
sudo -u n8n /opt/tts-env/bin/pip install anyascii coqpit fsspec humanize matplotlib numpy packaging pyyaml scipy inflect librosa phonemizer pysbd tqdm

echo "   - TTS (sem reinstalar dependências)..."
sudo -u n8n /opt/tts-env/bin/pip install TTS --no-deps

echo "   - Corrigindo dependências do TTS..."
sudo -u n8n /opt/tts-env/bin/pip install gruut==2.2.3 gruut-ipa==0.12.0

echo "   - MoviePy..."
sudo -u n8n /opt/tts-env/bin/pip install moviepy==1.0.3

echo "   - Whisper..."
sudo -u n8n /opt/tts-env/bin/pip install whisper-timestamped==1.14.2

# 10. Verifica instalação das dependências
echo "🔍 Verificando instalação..."
echo "   - Python: $(python3.11 --version)"
echo "   - Pip: $(/opt/tts-env/bin/pip --version)"
echo "   - Ambiente: /opt/tts-env"

MISSING_DEPS=()

if ! sudo -u n8n /opt/tts-env/bin/python3 -c "import flask" 2>/dev/null; then
    MISSING_DEPS+=("flask")
fi

if ! sudo -u n8n /opt/tts-env/bin/python3 -c "import torch" 2>/dev/null; then
    MISSING_DEPS+=("torch")
fi

if ! sudo -u n8n /opt/tts-env/bin/python3 -c "from TTS.api import TTS" 2>/dev/null; then
    MISSING_DEPS+=("TTS")
fi

if ! sudo -u n8n /opt/tts-env/bin/python3 -c "from moviepy.editor import *" 2>/dev/null; then
    MISSING_DEPS+=("moviepy")
fi

if ! sudo -u n8n /opt/tts-env/bin/python3 -c "import whisper_timestamped" 2>/dev/null; then
    MISSING_DEPS+=("whisper_timestamped")
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo "❌ Dependências em falta: ${MISSING_DEPS[*]}"
    echo "🔄 Tentando instalação alternativa..."
    
    # Fallback: instala versões mais recentes
    sudo -u n8n /opt/tts-env/bin/pip install flask torch TTS moviepy whisper-timestamped
    
    # Verifica novamente
    if ! sudo -u n8n /opt/tts-env/bin/python3 -c "from TTS.api import TTS" 2>/dev/null; then
        echo "❌ ERRO: TTS ainda não funciona. Instalação falhou."
        exit 1
    fi
fi

echo "✅ Todas as dependências instaladas com sucesso!"

# 11. Cria serviço systemd
echo "⚙️ Configurando serviço systemd..."
cat > /etc/systemd/system/video-automation.service << 'EOF'
[Unit]
Description=Video Automation Server
After=network.target

[Service]
Type=simple
User=n8n
Group=n8n
WorkingDirectory=/home/n8n/files
ExecStart=/opt/tts-env/bin/python3 /home/n8n/files/server.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/home/n8n/files
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# 12. Habilita e inicia serviço
echo "🚀 Iniciando serviço..."
systemctl daemon-reload
systemctl enable video-automation
systemctl start video-automation

# 13. Configura firewall
echo "🔥 Configurando firewall..."
ufw --force enable
ufw allow 22/tcp
ufw allow 5005/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# 14. Testa funcionamento
echo "🧪 Testando funcionamento..."

# Aguarda serviço iniciar
sleep 5

# Testa se o serviço está rodando
if systemctl is-active --quiet video-automation; then
    echo "✅ Serviço está rodando"
else
    echo "❌ Serviço não está rodando"
    systemctl status video-automation
    exit 1
fi

# Testa se está escutando na porta
if netstat -tlnp | grep -q ":5005"; then
    echo "✅ Servidor escutando na porta 5005"
else
    echo "❌ Servidor não está escutando na porta 5005"
    exit 1
fi

# Testa importação das bibliotecas
echo "🔍 Testando bibliotecas Python..."
if sudo -u n8n /opt/tts-env/bin/python3 -c "
from TTS.api import TTS
from moviepy.editor import *
import whisper_timestamped
print('✅ Todas as bibliotecas importadas com sucesso!')
"; then
    echo "✅ Bibliotecas funcionando"
else
    echo "❌ Erro na importação das bibliotecas"
    exit 1
fi

# Testa criação de arquivo nas pastas
echo "📁 Testando permissões de escrita..."
sudo -u n8n touch /files/imagens/teste.txt
sudo -u n8n touch /home/n8n/files/imagens/teste.txt

if [ -f "/files/imagens/teste.txt" ] && [ -f "/home/n8n/files/imagens/teste.txt" ]; then
    echo "✅ Permissões de escrita funcionando"
    # Remove arquivos de teste
    rm -f /files/imagens/teste.txt /home/n8n/files/imagens/teste.txt
else
    echo "❌ Erro nas permissões de escrita"
    exit 1
fi

# Testa endpoint de saúde
echo "🌐 Testando endpoint HTTP..."
if curl -s http://localhost:5005/health | grep -q "ok"; then
    echo "✅ Endpoint HTTP funcionando"
else
    echo "❌ Endpoint HTTP não está funcionando"
    exit 1
fi

# 15. Informações finais
echo ""
echo "================================"
echo "🎉 INSTALAÇÃO CONCLUÍDA!"
echo "================================"
echo ""
echo "🔗 Endpoints disponíveis:"
echo "   - POST http://SEU_IP:5005/create-video"
echo "   - GET  http://SEU_IP:5005/health"
echo "   - GET  http://SEU_IP:5005/status/<video_id>"
echo ""
echo "📂 Estrutura de pastas:"
echo "   - /files/imagens/     (para N8n salvar imagens)"
echo "   - /files/videos/      (vídeos gerados)"
echo "   - /files/fonts/       (fontes)"
echo ""
echo "🎬 Como usar:"
echo "   curl -X POST http://SEU_IP:5005/create-video \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"id\": \"teste001\", \"text\": \"Seu texto aqui\"}'"
echo ""
echo "📊 Status do serviço:"
systemctl status video-automation --no-pager -l
echo ""
echo "✅ Sistema pronto para uso!"