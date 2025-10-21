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

# 5. Limpeza completa (instalação do zero)
echo "🗑️ Limpando instalação anterior (se existir)..."
systemctl stop video-automation 2>/dev/null || true
systemctl disable video-automation 2>/dev/null || true
rm -rf /home/n8n/files/*
rm -rf /opt/tts-env
echo "✅ Sistema limpo, iniciando instalação do zero"

# 6. Cria diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p /home/n8n/files/audios
mkdir -p /home/n8n/files/imagens
mkdir -p /home/n8n/files/videos
mkdir -p /home/n8n/files/fonts
mkdir -p /files/audios
mkdir -p /files/imagens
mkdir -p /files/videos
mkdir -p /files/fonts

# 7. Baixar arquivos do GitHub
echo "📥 Baixando arquivos do GitHub..."
cd /tmp
rm -rf video-automation-n8n
git clone https://github.com/Paulolinks/video-automation-n8n.git
cp -r video-automation-n8n/files/* /home/n8n/files/
rm -rf video-automation-n8n
echo "✅ Arquivos copiados do GitHub"

# 8. Configura permissões (CORRIGIDO - lógica não sobrescreve)
echo "🔐 Configurando permissões..."

# Primeiro: dono n8n para TUDO
chown -R n8n:n8n /home/n8n/files
chmod -R 775 /home/n8n/files

# Depois: dono 1000 APENAS para pastas específicas que o Docker precisa
chown -R 1000:1000 /home/n8n/files/audios
chown -R 1000:1000 /home/n8n/files/videos  
chown -R 1000:1000 /home/n8n/files/imagens

# Permissões para /files (symlink do Docker)
chown -R n8n:n8n /files
chown -R 1000:1000 /files/audios
chown -R 1000:1000 /files/videos
chown -R 1000:1000 /files/imagens
chmod -R 775 /files

echo "✅ Permissões configuradas: n8n (geral) + 1000 (pastas específicas)"

# 9. Cria ambiente virtual com Python 3.11 FORÇADO
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

# 10. Atualiza pip
echo "📦 Atualizando pip..."
sudo -u n8n /opt/tts-env/bin/pip install --upgrade pip

# 11. Instala dependências Python NA ORDEM CORRETA
echo "📦 Instalando dependências Python com versões compatíveis..."

echo "   - Flask..."
sudo -u n8n /opt/tts-env/bin/pip install flask==3.0.0

echo "   - PyTorch 2.1 (compatível com XTTS_v2)..."
sudo -u n8n /opt/tts-env/bin/pip install torch==2.1.0 torchaudio==2.1.0

echo "   - TTS (com todas as dependências)..."
sudo -u n8n /opt/tts-env/bin/pip install TTS

echo "   - MoviePy..."
sudo -u n8n /opt/tts-env/bin/pip install moviepy==1.0.3

echo "   - Whisper..."
sudo -u n8n /opt/tts-env/bin/pip install whisper-timestamped==1.14.2

echo "   - Pillow (para MoviePy processar imagens)..."
sudo -u n8n /opt/tts-env/bin/pip install Pillow==9.5.0

# 11.1. CORREÇÃO CRÍTICA: Instala versão correta do transformers para XTTS_v2
echo "   - Corrigindo transformers para compatibilidade com XTTS_v2..."
sudo -u n8n /opt/tts-env/bin/pip uninstall -y transformers 2>/dev/null || true
sudo -u n8n /opt/tts-env/bin/pip install transformers==4.33.0

echo "✅ Transformers 4.33.0 instalado (compatível com XTTS_v2)"

# 12. Verifica instalação das dependências
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

# 13. Cria serviço systemd
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

# 14. Habilita e inicia serviço
echo "🚀 Iniciando serviço..."
systemctl daemon-reload
systemctl enable video-automation
systemctl start video-automation

# 15. Configura firewall
echo "🔥 Configurando firewall..."
ufw --force enable
ufw allow 22/tcp
ufw allow 5005/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# 16. Testa funcionamento
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

# Garantir permissões finais (crítico após restart/updates)
echo "🔐 Aplicando permissões finais..."

# Primeiro: dono n8n para TUDO
chown -R n8n:n8n /home/n8n/files
chmod -R 775 /home/n8n/files

# Depois: dono 1000 APENAS para pastas específicas
chown -R 1000:1000 /home/n8n/files/audios
chown -R 1000:1000 /home/n8n/files/videos
chown -R 1000:1000 /home/n8n/files/imagens

# Permissões para /files (symlink do Docker)
chown -R n8n:n8n /files
chown -R 1000:1000 /files/audios
chown -R 1000:1000 /files/videos
chown -R 1000:1000 /files/imagens
chmod -R 775 /files

echo "✅ Permissões finais aplicadas"

# Verificação e correção FORÇADA de permissões
echo "🔍 Verificando e corrigindo permissões..."

# Diagnóstico: ver o que está interferindo
echo "🔍 Diagnóstico de interferências..."
echo "   Processos que podem interferir:"
ps aux | grep -E "(chown|chmod|ubuntu)" | grep -v grep || echo "   Nenhum processo suspeito encontrado"
echo "   Mounts especiais:"
mount | grep -E "(n8n|files)" || echo "   Nenhum mount especial encontrado"

for i in {1..5}; do
    echo "🔄 Tentativa $i/5 de correção de permissões..."
    
    # Força permissões novamente
    chown -R n8n:n8n /home/n8n/files
    chmod -R 775 /home/n8n/files
    chown -R 1000:1000 /home/n8n/files/audios
    chown -R 1000:1000 /home/n8n/files/videos
    chown -R 1000:1000 /home/n8n/files/imagens
    
    # Verifica se funcionou
    AUDIOS_OWNER=$(stat -c '%U' /home/n8n/files/audios)
    VIDEOS_OWNER=$(stat -c '%U' /home/n8n/files/videos)
    IMAGENS_OWNER=$(stat -c '%U' /home/n8n/files/imagens)
    
    echo "   audios: $AUDIOS_OWNER, videos: $VIDEOS_OWNER, imagens: $IMAGENS_OWNER"
    
    if [ "$AUDIOS_OWNER" = "1000" ] && [ "$VIDEOS_OWNER" = "1000" ] && [ "$IMAGENS_OWNER" = "1000" ]; then
        echo "✅ Permissões corrigidas com sucesso!"
        break
    fi
    
    if [ $i -eq 5 ]; then
        echo "❌ ERRO: Não foi possível corrigir permissões após 5 tentativas"
        echo "   audios: $AUDIOS_OWNER (esperado: 1000)"
        echo "   videos: $VIDEOS_OWNER (esperado: 1000)"
        echo "   imagens: $IMAGENS_OWNER (esperado: 1000)"
        exit 1
    fi
    
    echo "   ⏳ Aguardando 2 segundos antes da próxima tentativa..."
    sleep 2
done

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

# Testa criação de áudio
echo "🎤 Testando criação de áudio..."
AUDIO_RESPONSE=$(curl -s -X POST http://localhost:5005/create-audio \
  -H "Content-Type: application/json" \
  -d '{"id": "teste_instalacao", "text": "Teste de instalação automática"}')

if echo "$AUDIO_RESPONSE" | grep -q "error"; then
    echo "❌ Erro ao testar criação de áudio: $AUDIO_RESPONSE"
    exit 1
fi
echo "✅ Criação de áudio funcionando"

# 17. Informações finais
echo ""
echo "================================"
echo "🎉 INSTALAÇÃO CONCLUÍDA!"
echo "================================"
echo ""
echo "🔗 Endpoints disponíveis:"
echo "   - POST http://SEU_IP:5005/create-audio"
echo "   - POST http://SEU_IP:5005/create-video"
echo "   - GET  http://SEU_IP:5005/health"
echo "   - GET  http://SEU_IP:5005/status/<video_id>"
echo ""
echo "📂 Estrutura de pastas:"
echo "   - /files/audios/      (áudios gerados)"
echo "   - /files/imagens/     (para N8n salvar imagens)"
echo "   - /files/videos/      (vídeos gerados)"
echo "   - /files/fonts/       (fontes)"
echo ""
echo "🎬 Como usar:"
echo "   # Limpar imagens corrompidas:"
echo "   curl -X POST http://SEU_IP:5005/clean-images"
echo ""
echo "   # Criar áudio:"
echo "   curl -X POST http://SEU_IP:5005/create-audio \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"id\": \"audio001\", \"text\": \"Seu texto aqui\"}'"
echo ""
echo "   # Criar vídeo:"
echo "   curl -X POST http://SEU_IP:5005/create-video \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"id\": \"video001\"}'"
echo ""
echo "📊 Status do serviço:"
systemctl status video-automation --no-pager -l
echo ""
echo "✅ Sistema pronto para uso!"