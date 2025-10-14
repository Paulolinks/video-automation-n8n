# 🎬 Video Automation System

Sistema profissional de automação de vídeos com clonagem de voz, legendas automáticas e formato Reels (9:16).

## ✨ Características

- **🎤 Clonagem de Voz**: Usa TTS (XTTS_v2) para clonar sua voz
- **📝 Legendas Automáticas**: Whisper gera legendas com timestamps
- **🎨 Formato Reels**: Vídeos otimizados para Instagram/TikTok
- **⚡ Arquitetura Profissional**: Servidor separado do processamento
- **🔧 Instalação Automática**: Um comando instala tudo
- **🌐 API REST**: Integração fácil com N8n e outras ferramentas

## 🏗️ Arquitetura

```
┌─────────────────┐           ┌─────────────────┐
│   N8n/Cliente   │           │   server.py     │
│                 │           │ (Flask Server)  │
│  1. create-audio│──HTTP────►│  Port 5005      │
│  2. create-video│           └─────────────────┘
└─────────────────┘                    │
                                       │ subprocess
                          ┌────────────┴────────────┐
                          ▼                         ▼
                ┌──────────────────┐    ┌──────────────────┐
                │ create_audio.py  │    │ create_video.py  │
                │ (TTS + Voice     │    │ (MoviePy +       │
                │  Cloning)        │    │  Whisper)        │
                └──────────────────┘    └──────────────────┘
                          │                         │
                          ▼                         ▼
                    audios/                   videos/
```

### Componentes

- **`server.py`**: Servidor Flask com 2 endpoints separados
  - `/create-audio`: Gera áudio com clonagem de voz
  - `/create-video`: Gera vídeo com legendas
- **`create_audio.py`**: Script isolado para TTS (XTTS_v2)
- **`create_video.py`**: Script isolado para criação de vídeo
- **`INSTALL_VPS.sh`**: Instalação automática completa
- **`voice_sample.wav`**: Arquivo de voz para clonagem

### Estrutura de Pastas

```
/home/n8n/files/
├── audios/          # Áudios gerados pelo TTS
├── imagens/         # Imagens baixadas pelo N8n
├── videos/          # Vídeos finais
├── fonts/           # Fontes para legendas
├── voice_sample.wav # Amostra de voz
├── server.py        # Servidor Flask
├── create_audio.py  # Script TTS
└── create_video.py  # Script vídeo
```

## 🚀 Instalação Super Rápida

### Para Usuários (2 comandos)

```bash
# 1. Baixar e instalar automaticamente
sudo curl -sSL https://raw.githubusercontent.com/Paulolinks/video-automation-n8n/master/files/quick_install.sh | bash

# 2. Pronto! Sistema funcionando
```

### Para Desenvolvedores

```bash
# Clone o repositório
git clone https://github.com/Paulolinks/video-automation-n8n.git
cd video-automation-n8n/files

# Execute a instalação
sudo ./INSTALL_VPS.sh
```

## 📋 Requisitos do Sistema

- **Ubuntu 20.04+** (testado em Hostinger VPS)
- **8GB RAM** (mínimo 4GB)
- **Python 3.11** (instalado automaticamente)
- **20GB espaço** (para dependências e vídeos)

## 🔧 O que a Instalação Faz

A instalação automática:

1. ✅ **Atualiza o sistema**
2. ✅ **Instala Python 3.11**
3. ✅ **Instala FFmpeg e dependências**
4. ✅ **Cria usuário n8n**
5. ✅ **Configura permissões**
6. ✅ **Instala TTS com clonagem de voz**
7. ✅ **Instala MoviePy e Whisper**
8. ✅ **Configura serviço systemd**
9. ✅ **Configura firewall**
10. ✅ **Testa funcionamento completo**

## 🌐 Endpoints da API

### 1. Criar Áudio (Passo 1)
```bash
POST /create-audio
Content-Type: application/json

{
  "id": "video001",
  "text": "Seu texto aqui para gerar o áudio com sua voz clonada"
}
```

**Resposta:**
```json
{
  "status": "started",
  "audio_id": "video001",
  "message": "Criação de áudio iniciada com sucesso!",
  "audio_path": "/audios/audio_video001.wav"
}
```

### 2. Criar Vídeo (Passo 2)
```bash
POST /create-video
Content-Type: application/json

{
  "id": "video001"
}
```

**Nota:** O áudio e as imagens devem estar prontos antes de chamar este endpoint.

**Resposta:**
```json
{
  "status": "started",
  "video_id": "video001",
  "message": "Criação de vídeo iniciada com sucesso!",
  "images_found": 6
}
```

### 3. Verificar Status
```bash
GET /status/<id>
```

### Saúde do Sistema
```bash
GET /health
```

### Download de Arquivo
```bash
GET /download/<filename>
```

## 📁 Estrutura de Pastas

```
/home/n8n/files/
├── server.py              # Servidor Flask
├── create_video.py        # Processamento de vídeo
├── voice_sample.wav       # Voz para clonagem
├── requirements.txt       # Dependências Python
├── imagens/               # Imagens para o vídeo
├── videos/                # Vídeos gerados
└── fonts/                 # Fontes para legendas

/files/                    # Pastas para N8n
├── imagens/               # N8n salva imagens aqui
├── videos/                # Vídeos acessíveis
└── fonts/                 # Fontes acessíveis
```

## 🎯 Como Usar

### 1. Criar Áudio
```bash
curl -X POST http://SEU_IP:5005/create-audio \
  -H "Content-Type: application/json" \
  -d '{
    "id": "meu_video_001",
    "text": "Seu texto aqui"
  }'
```

### 2. Preparar Imagens
Coloque suas imagens na pasta `/files/imagens/`:
```bash
# Exemplo de estrutura
/files/imagens/
├── image_01.jpg
├── image_02.jpg
└── image_03.jpg
```

### 3. Criar Vídeo
```bash
curl -X POST http://SEU_IP:5005/create-video \
  -H "Content-Type: application/json" \
  -d '{"id": "meu_video_001"}'
```

### 4. Verificar Status
```bash
curl http://SEU_IP:5005/status/meu_video_001
```

### 4. Baixar Vídeo
```bash
curl -O http://SEU_IP:5005/download/videos/video_meu_video_001.mp4
```

## 🔗 Integração com N8n

### Workflow Recomendado

```
1. [Buscar Dados]
     ↓
2. [HTTP - Criar Áudio]
     ↓
3. [Wait 60s]
     ↓
4. [HTTP - Baixar Imagens]
     ↓
5. [Wait 10s]
     ↓
6. [HTTP - Criar Vídeo]
     ↓
7. [Wait 180s]
     ↓
8. [HTTP - Download Vídeo]
```

### 1. Node: Criar Áudio

**HTTP Request Node**:
- **URL**: `http://SEU_IP:5005/create-audio`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:
  ```json
  {
    "id": "{{ $json.id }}",
    "text": "{{ $json.texto }}"
  }
  ```

### 2. Node: Wait (60 segundos)

Aguarde o áudio ser gerado.

### 3. Node: Baixar Imagens

Use sua API de imagens (Pexels, etc.) e salve em `/files/imagens/`.

### 4. Node: Wait (10 segundos)

Aguarde as imagens serem salvas.

### 5. Node: Criar Vídeo

**HTTP Request Node**:
- **URL**: `http://SEU_IP:5005/create-video`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:
  ```json
  {
    "id": "{{ $json.id }}"
  }
  ```

### 6. Node: Wait (180 segundos)

Aguarde o vídeo ser gerado.

### 7. Node: Download Vídeo

**HTTP Request Node**:
- **URL**: `http://SEU_IP:5005/download/videos/video_{{ $json.id }}.mp4`
- **Method**: `GET`
- **Response Format**: `File`

### Dicas Importantes

- **IDs únicos**: Use `{{ $json.row_number }}` ou `{{ $now.format('YYYYMMDD-HHmmss') }}`
- **Nunca reutilize IDs**: Cada vídeo precisa de um ID único
- **Aguarde os processos**: TTS e MoviePy demoram alguns minutos
- **Salvar imagens primeiro**: O vídeo precisa das imagens já salvas

## ⚙️ Configurações Avançadas

### Alterar Fonte das Legendas
Edite `create_video.py`:
```python
FONT_NAME = "SuaFonteAqui"  # Linha 18
```

### Alterar Formato do Vídeo
Edite `create_video.py`:
```python
VIDEO_WIDTH = 1080   # Linha 15
VIDEO_HEIGHT = 1920  # Linha 16
```

### Timeout de Processamento
Edite `server.py`:
```python
timeout=600  # 10 minutos (linha 45)
```

## 🐛 Solução de Problemas

### Serviço não inicia
```bash
sudo systemctl status video-automation
sudo journalctl -u video-automation -n 50
```

### Problemas de Permissão
```bash
sudo chown -R n8n:n8n /files
sudo chown -R n8n:n8n /home/n8n/files
```

### Porta 5005 não acessível
```bash
# Verificar firewall
sudo ufw status
sudo ufw allow 5005/tcp
```

### TTS não funciona
```bash
# Verificar Python 3.11
python3.11 --version

# Reinstalar TTS
sudo /opt/tts-env/bin/pip install TTS==0.22.0
```

## 📊 Monitoramento

### Logs do Servidor
```bash
sudo journalctl -u video-automation -f
```

### Uso de Recursos
```bash
# CPU e Memória
htop

# Espaço em disco
df -h

# Processos Python
ps aux | grep python
```

## 🔄 Atualizações

### Reinstalar Sistema
```bash
# Limpar instalação anterior
sudo curl -sSL https://raw.githubusercontent.com/Paulolinks/video-automation-n8n/master/files/cleanup.sh | bash

# Reinstalar
sudo curl -sSL https://raw.githubusercontent.com/Paulolinks/video-automation-n8n/master/files/quick_install.sh | bash
```

## 📞 Suporte

- **GitHub Issues**: [Abrir Issue](https://github.com/Paulolinks/video-automation-n8n/issues)
- **Documentação**: Este README
- **Logs**: `sudo journalctl -u video-automation`

## 📄 Licença

Este projeto é de uso livre para automações pessoais e comerciais.

---

**🎬 Crie vídeos profissionais com sua voz em segundos!**