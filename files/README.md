# 🎬 Video Automation Server

Sistema automatizado para criação de vídeos com:
- Clonagem de voz usando XTTS
- Geração automática de legendas
- Slides de imagens sincronizados
- Formato Reels (9:16)

## 📋 Requisitos

- Python 3.8+
- FFmpeg
- ImageMagick

## 🚀 Instalação no VPS (2 comandos apenas!)

### Opção 1: Instalação Super Rápida (Recomendado)
```bash
# 1. Baixa e instala tudo de uma vez
sudo curl -sSL https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPO/main/quick_install.sh | bash

# 2. Copie seus arquivos
scp voice_sample.wav root@seu_ip:/home/n8n/files/
scp -r fonts/* root@seu_ip:/home/n8n/files/fonts/
```

### Opção 2: Instalação Manual
```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/SEU_REPO.git
cd SEU_REPO/files

# 2. Execute o instalador
sudo chmod +x INSTALL_VPS.sh
sudo ./INSTALL_VPS.sh
```

### Opção 3: Instalação Passo a Passo
```bash
# Instale dependências
sudo apt update
sudo apt install -y python3-pip python3-venv ffmpeg imagemagick git

# Configure ImageMagick
sudo sed -i 's/<policy domain="path" rights="none" pattern="@\*"\/>/<\!-- <policy domain="path" rights="none" pattern="@\*"\/> -->/' /etc/ImageMagick-6/policy.xml

# Crie ambiente virtual
python3 -m venv /opt/tts-env
source /opt/tts-env/bin/activate

# Instale dependências Python
pip install --upgrade pip
pip install -r requirements.txt

# Configure o serviço
sudo cp INSTALL_VPS.sh /tmp/ && sudo /tmp/INSTALL_VPS.sh
```

## 🔗 Uso com N8n

### HTTP Request
- **Method**: POST
- **URL**: `http://SEU_IP:5005/create-video`
- **Body**:
```json
{
  "id": "123",
  "text": "Seu texto aqui"
}
```

### Resposta
```json
{
  "status": "ok",
  "video_file": "/files/video_123.mp4",
  "audio_file": "/files/audio_123.wav"
}
```

## 📂 Estrutura de Pastas

```
/home/n8n/files/
├── video_automation.py    # Servidor principal
├── requirements.txt       # Dependências
├── INSTALL_VPS.sh         # Instalador automático
├── quick_install.sh       # Instalador super rápido
├── voice_sample.wav       # Amostra de voz para clonagem
├── fonts/                 # Fontes para legendas
│   ├── anton.ttf
│   ├── Active_Heart.ttf
│   └── ...
├── imagens/              # Imagens para o vídeo (colocadas pelo N8n)
│   └── image_*.jpg
└── videos/               # Vídeos gerados (limpeza automática)
    └── video_*.mp4
```

## 🔍 Logs

```bash
sudo journalctl -u video-automation -f
```

## 📝 Checklist

- [ ] Python 3.8+ instalado
- [ ] FFmpeg instalado
- [ ] ImageMagick configurado
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] voice_sample.wav presente
- [ ] Pasta imagens/ criada
- [ ] Fontes copiadas
- [ ] Serviço systemd configurado
- [ ] Porta 5005 liberada no firewall

