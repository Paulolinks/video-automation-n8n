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
