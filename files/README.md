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
┌─────────────────┐    HTTP     ┌─────────────────┐
│   N8n/Cliente   │ ──────────► │   server.py     │
└─────────────────┘             │ (Flask Server)  │
                                └─────────────────┘
                                         │
                                         ▼ subprocess
                                ┌─────────────────┐
                                │ create_video.py │
                                │ (Processamento) │
                                └─────────────────┘
```

### Componentes

- **`server.py`**: Servidor Flask que recebe requisições HTTP
- **`create_video.py`**: Processamento completo de vídeo
- **`INSTALL_VPS.sh`**: Instalação automática completa
- **`voice_sample.wav`**: Arquivo de voz para clonagem

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

### Criar Vídeo
```bash
POST /create-video
Content-Type: application/json

{
  "id": "video001",
  "text": "Seu texto aqui para gerar o vídeo com sua voz clonada"
}
```

### Verificar Status
```bash
GET /status/<video_id>
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

### 1. Preparar Imagens
Coloque suas imagens na pasta `/files/imagens/`:
```bash
# Exemplo de estrutura
/files/imagens/
├── image_01.jpg
├── image_02.jpg
└── image_03.jpg
```

### 2. Criar Vídeo via API
```bash
curl -X POST http://SEU_IP:5005/create-video \
  -H "Content-Type: application/json" \
  -d '{
    "id": "meu_video_001",
    "text": "Acredite no seu processo. Cada passo que você dá hoje aproxima você do seu próximo nível. Continue avançando sempre."
  }'
```

### 3. Verificar Status
```bash
curl http://SEU_IP:5005/status/meu_video_001
```

### 4. Baixar Vídeo
```bash
curl -O http://SEU_IP:5005/download/videos/video_meu_video_001.mp4
```

## 🔗 Integração com N8n

### Configuração no N8n

1. **HTTP Request Node**:
   - **URL**: `http://SEU_IP:5005/create-video`
   - **Method**: POST
   - **Body**:
     ```json
     {
       "id": "{{ $json.id }}",
       "text": "{{ $json.text }}"
     }
     ```

2. **Salvar Imagens**:
   - Use a pasta `/files/imagens/` no seu workflow
   - O N8n pode escrever diretamente nesta pasta

3. **Buscar Vídeo**:
   - Vídeos são salvos em `/files/videos/`
   - Use HTTP Request para baixar: `/download/videos/video_ID.mp4`

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