# 🧪 TESTES NO TERMINAL

## 📋 **PRÉ-REQUISITOS**

1. Servidor Flask rodando (`python3 server.py` ou via systemd)
2. Pasta `imagens/` com imagens
3. Arquivo `voice_sample.wav` presente

---

## 🎤 **TESTE 1: CRIAR ÁUDIO**

### **Comando:**
```bash
curl -X POST http://localhost:5005/create-audio \
  -H "Content-Type: application/json" \
  -d '{
    "id": "teste_001",
    "text": "O universo está sempre respondendo às suas vibrações. Mas você está ouvindo? O silêncio é a linguagem do coração. Acalme sua mente e escute o que ele tem a dizer. Só então você começará a criar realidade."
  }'
```

### **Resposta esperada:**
```json
{
  "status": "started",
  "audio_id": "teste_001",
  "message": "Criação de áudio iniciada com sucesso!",
  "audio_path": "/audios/audio_teste_001.wav"
}
```

### **Verificar status:**
```bash
curl http://localhost:5005/status/teste_001
```

### **Aguarde 30-60 segundos** até o status mudar para `completed`

### **Verificar arquivo criado:**
```bash
ls -lh audios/audio_teste_001.wav
```

---

## 🎬 **TESTE 2: CRIAR VÍDEO**

### **Comando:**
```bash
curl -X POST http://localhost:5005/create-video \
  -H "Content-Type: application/json" \
  -d '{"id": "teste_001"}'
```

### **Resposta esperada:**
```json
{
  "status": "started",
  "video_id": "teste_001",
  "message": "Criação de vídeo iniciada com sucesso!",
  "images_found": 6
}
```

### **Verificar status:**
```bash
curl http://localhost:5005/status/teste_001
```

### **Aguarde 2-3 minutos** até o status mudar para `completed`

### **Verificar arquivo criado:**
```bash
ls -lh videos/video_teste_001.mp4
```

---

## 🧪 **TESTE COMPLETO (Áudio + Vídeo)**

### **Script bash:**
```bash
#!/bin/bash

ID="teste_$(date +%Y%m%d_%H%M%S)"
TEXTO="Este é um teste completo do sistema de automação. O áudio será gerado com clonagem de voz, e o vídeo incluirá legendas automáticas sincronizadas com as imagens."

echo "======================================"
echo "🎬 TESTE COMPLETO - ID: $ID"
echo "======================================"

# 1. Criar áudio
echo ""
echo "1️⃣ Criando áudio..."
curl -X POST http://localhost:5005/create-audio \
  -H "Content-Type: application/json" \
  -d "{\"id\": \"$ID\", \"text\": \"$TEXTO\"}"

echo ""
echo "⏳ Aguardando 60 segundos para áudio ser gerado..."
sleep 60

# 2. Verificar status do áudio
echo ""
echo "2️⃣ Verificando status do áudio..."
curl http://localhost:5005/status/$ID

# 3. Criar vídeo
echo ""
echo ""
echo "3️⃣ Criando vídeo..."
curl -X POST http://localhost:5005/create-video \
  -H "Content-Type: application/json" \
  -d "{\"id\": \"$ID\"}"

echo ""
echo "⏳ Aguardando 180 segundos para vídeo ser gerado..."
sleep 180

# 4. Verificar status do vídeo
echo ""
echo "4️⃣ Verificando status do vídeo..."
curl http://localhost:5005/status/$ID

# 5. Listar arquivos gerados
echo ""
echo ""
echo "======================================"
echo "📁 ARQUIVOS GERADOS:"
echo "======================================"
ls -lh audios/audio_$ID.wav
ls -lh videos/video_$ID.mp4

echo ""
echo "✅ TESTE CONCLUÍDO!"
```

**Salve como `teste_completo.sh` e execute:**
```bash
chmod +x teste_completo.sh
./teste_completo.sh
```

---

## 🌐 **TESTE NO VPS (Remoto)**

### **Substitua `localhost` pelo IP do seu VPS:**

```bash
# Exemplo:
curl -X POST http://31.97.142.45:5005/create-audio \
  -H "Content-Type: application/json" \
  -d '{
    "id": "teste_vps_001",
    "text": "Teste remoto no VPS com clonagem de voz."
  }'
```

---

## 📊 **MONITORAR LOGS EM TEMPO REAL**

### **Se rodando via systemd:**
```bash
sudo journalctl -u video-automation -f
```

### **Se rodando manualmente:**
```bash
# Em um terminal, inicie o servidor:
python3 server.py

# Em outro terminal, execute os testes
curl -X POST http://localhost:5005/create-audio ...
```

---

## 🔧 **COMANDOS ÚTEIS**

### **Ver processos ativos:**
```bash
curl http://localhost:5005/health
```

### **Baixar áudio gerado:**
```bash
curl -O http://localhost:5005/download/audios/audio_teste_001.wav
```

### **Baixar vídeo gerado:**
```bash
curl -O http://localhost:5005/download/videos/video_teste_001.mp4
```

### **Limpar arquivos antigos:**
```bash
# Limpar áudios
rm -f audios/*.wav

# Limpar vídeos
rm -f videos/*.mp4
```

---

## ⚠️ **SOLUÇÃO DE PROBLEMAS**

### **Erro: "Áudio não encontrado"**
- Verifique se o áudio foi criado: `ls -lh audios/`
- Aguarde mais tempo para o áudio ser gerado (30-60s)
- Verifique os logs do servidor

### **Erro: "Nenhuma imagem encontrada"**
- Adicione imagens na pasta `imagens/`: `ls -lh imagens/`
- Certifique-se de que as imagens são .jpg, .jpeg ou .png

### **Erro: "Voice sample não encontrado"**
- Verifique se `voice_sample.wav` existe: `ls -lh voice_sample.wav`
- O arquivo deve estar na mesma pasta que `server.py`

### **Vídeo não é criado (timeout)**
- Aumente o tempo de espera para 5 minutos
- Verifique se há memória RAM suficiente: `free -h`
- Reduza o número de imagens para 3-5

---

## ✅ **RESULTADO ESPERADO**

Após executar os testes:
- ✅ Áudio em `audios/audio_teste_001.wav`
- ✅ Vídeo em `videos/video_teste_001.mp4`
- ✅ Vídeo no formato Reels (1080x1920)
- ✅ Áudio com voz clonada
- ✅ Legendas sincronizadas (se Whisper funcionar)

