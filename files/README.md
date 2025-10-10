<<<<<<< HEAD
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

=======
# 🎬 Sistema de Criação Automática de Vídeos

Sistema completo para criação automática de vídeos com legendas, integrado ao N8n para automação de redes sociais.

## 🚀 Funcionalidades

- ✅ **TTS de Alta Qualidade** - Usa XTTS v2 para voz natural
- ✅ **Legendas Automáticas** - Whisper para transcrição e timing
- ✅ **Múltiplas Fontes** - 9 fontes personalizadas disponíveis
- ✅ **Suporte a Imagens e Vídeos** - Criação com ambos os tipos de mídia
- ✅ **Interface Web** - Configuração fácil via navegador
- ✅ **API REST** - Integração completa com N8n
- ✅ **Otimizado para VPS** - Consumo de memória otimizado

## 📋 Requisitos do VPS

- **RAM**: 8GB (mínimo 4GB)
- **CPU**: 2 cores
- **HD**: 100GB
- **SO**: Ubuntu 20.04+ ou Debian 11+
- **Python**: 3.9+

## 🛠️ Instalação Rápida

1. **Faça upload dos arquivos para o VPS:**
```bash
scp -r files/ user@seu_vps_ip:/home/n8n/
```

2. **Execute o script de instalação:**
```bash
ssh user@seu_vps_ip
cd /home/n8n/files
chmod +x install_vps.sh
sudo ./install_vps.sh
```

3. **Acesse a interface web:**
```
http://SEU_VPS_IP:5006
```

## 🔧 Configuração

### 1. **Coloque sua amostra de voz:**
```bash
# Copie seu arquivo de voz para:
/home/n8n/files/voice_sample.wav
```

### 2. **Adicione imagens/vídeos:**
```bash
# Para vídeos com imagens:
/home/n8n/files/imagens/

# Para vídeos com vídeos:
/home/n8n/files/videos/
```

### 3. **Configure via interface web:**
- Acesse `http://SEU_VPS_IP:5006`
- Escolha fonte, tipo de vídeo, qualidade, etc.

## 📡 API Endpoints

### **GET /health**
Verifica status do servidor
```bash
curl http://SEU_VPS_IP:5005/health
```

### **GET /fonts**
Lista fontes disponíveis
```bash
curl http://SEU_VPS_IP:5005/fonts
```

### **POST /generate-audio**
Gera áudio com TTS
```json
{
  "frase": "Seu texto aqui",
  "id": "123"
}
```

### **POST /generate-video**
Gera vídeo completo
```json
{
  "frase": "Seu texto aqui",
  "id": "123",
  "font": "Anton",
  "type": "images"
}
```

## 🔄 Integração com N8n

### **Workflow Básico:**
1. **Trigger** - Agendamento ou webhook
2. **Google Sheets** - Busca conteúdo
3. **Condição** - Verifica se deve processar
4. **Gerar Áudio** - Chama API `/generate-audio`
5. **Gerar Vídeo** - Chama API `/generate-video`
6. **Upload** - Envia para Google Drive
7. **Atualizar** - Marca como processado

### **Exemplo de Nó HTTP Request:**
```json
{
  "url": "http://SEU_VPS_IP:5005/generate-video",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "frase": "={{ $json.texto }}",
    "id": "={{ $json.id }}",
    "font": "Anton",
    "type": "images"
  }
}
```

## 🎨 Fontes Disponíveis

- **Active_Heart** - Estilo coração
- **Anton** - Sans-serif moderna
- **Bold** - Negrito clássico
- **Loucos** - Estilo criativo
- **Loucos2** - Variação criativa
- **New** - Estilo novo
- **Thequir** - Estilo único
- **Typo** - Tipográfica
- **Wallman_Bold** - Negrito estilizado

## ⚡ Otimizações para VPS

### **Uso de Memória:**
- Scripts otimizados com `gc.collect()`
- Processamento em lotes
- Limpeza automática de objetos

### **Qualidade de Vídeo:**
- **Baixa**: Rápido, menor qualidade
- **Média**: Equilíbrio (recomendado)
- **Alta**: Lento, melhor qualidade

### **Configurações Recomendadas:**
```json
{
  "video_quality": "medium",
  "subtitle_size": 72,
  "subtitle_color": "yellow"
}
```

## 🔍 Monitoramento

### **Verificar Status:**
```bash
sudo systemctl status video-creator
sudo systemctl status video-web
```

### **Ver Logs:**
```bash
sudo journalctl -u video-creator -f
sudo journalctl -u video-web -f
```

### **Reiniciar Serviços:**
```bash
sudo systemctl restart video-creator
sudo systemctl restart video-web
```

## 🐛 Solução de Problemas

### **Erro de Memória:**
- Use `make_video_optimized.py`
- Reduza qualidade do vídeo
- Processe menos imagens por vez

### **Erro de Fonte:**
- Verifique se a fonte está instalada
- Use `fc-list | grep -i nome_da_fonte`

### **Erro de Áudio:**
- Verifique se `voice_sample.wav` existe
- Teste com arquivo de áudio menor

## 📁 Estrutura de Arquivos

```
/home/n8n/files/
├── server.py                 # API principal
├── web_interface.py          # Interface web
├── make_video.py            # Criação com imagens
├── make_video_optimized.py  # Versão otimizada
├── make_video_with_videos.py # Criação com vídeos
├── tts_audio_highquality.py # TTS de alta qualidade
├── add_subtitles.py         # Adicionar legendas
├── transcribe.py            # Transcrição
├── install_vps.sh           # Script de instalação
├── config.json              # Configurações
├── fonts/                   # Fontes personalizadas
├── templates/               # Interface web
├── imagens/                 # Imagens para vídeos
├── videos/                  # Vídeos para composição
└── voice_sample.wav         # Sua amostra de voz
```

## 🚀 Próximos Passos

1. **Configure seu VPS** com o script de instalação
2. **Adicione sua amostra de voz** em `voice_sample.wav`
3. **Teste a API** com curl ou Postman
4. **Configure o N8n** com o workflow de exemplo
5. **Adicione conteúdo** nas pastas de imagens/vídeos
6. **Monitore os logs** para verificar funcionamento

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs do sistema
2. Teste os endpoints da API
3. Verifique se todos os arquivos estão no lugar
4. Confirme se os serviços estão rodando

---

**🎬 Seu sistema de criação automática de vídeos está pronto!**
>>>>>>> 19ec738a439d4cdd78105e8c18c6114669f18a2c
