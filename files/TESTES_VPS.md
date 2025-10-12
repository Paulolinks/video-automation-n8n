# 🧪 COMANDOS DE TESTE - VPS

## 📋 **Comandos Úteis para Testar e Monitorar**

### **1. Testar Saúde do Servidor**
```bash
curl http://localhost:5005/health
curl http://31.97.142.45:5005/health
```

**Resposta esperada:**
```json
{"active_processes":0,"message":"Video Automation Server is running","status":"ok"}
```

---

### **2. Criar Vídeo (Teste Simples)**
```bash
curl -X POST http://31.97.142.45:5005/create-video \
  -H "Content-Type: application/json" \
  -d '{"id": "teste001", "text": "Este é um teste rápido do sistema de automação de vídeos com clonagem de voz XTTS_v2."}'
```

**Resposta esperada:**
```json
{"images_found":6,"message":"Criação de vídeo iniciada com sucesso!","status":"started","video_id":"teste001"}
```

---

### **3. Verificar Status do Vídeo**
```bash
curl http://31.97.142.45:5005/status/teste001
```

**Respostas possíveis:**
- `"status": "running"` - Processando
- `"status": "completed"` - Concluído
- `"status": "error"` - Erro
- `"status": "not_found"` - ID não encontrado

---

### **4. Ver Logs em Tempo Real**
```bash
sudo journalctl -u video-automation -f
```
**Mostra:** Tudo que está acontecendo em tempo real

**Para sair:** Pressione `Ctrl+C`

---

### **5. Ver Últimas 50 Linhas dos Logs**
```bash
sudo journalctl -u video-automation -n 50 --no-pager
```

---

### **6. Verificar Vídeos Criados**
```bash
ls -lh /home/n8n/files/videos/
```

---

### **7. Baixar Vídeo para seu PC**
```bash
# Do seu PC (não do VPS):
scp root@31.97.142.45:/home/n8n/files/videos/video_teste001.mp4 .
```

---

### **8. Gerenciar o Serviço**

```bash
# Ver status
sudo systemctl status video-automation

# Parar
sudo systemctl stop video-automation

# Iniciar
sudo systemctl start video-automation

# Reiniciar
sudo systemctl restart video-automation

# Desabilitar (não inicia automaticamente)
sudo systemctl disable video-automation

# Habilitar (inicia no boot)
sudo systemctl enable video-automation
```

---

### **9. Limpar Vídeos Antigos**
```bash
# Deletar todos os vídeos
rm -f /home/n8n/files/videos/*.mp4

# Deletar vídeos específicos
rm -f /home/n8n/files/videos/video_teste*.mp4
```

---

### **10. Testar TTS Isoladamente**
```bash
sudo -u n8n /opt/tts-env/bin/python3 << 'EOF'
from TTS.api import TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
tts.tts_to_file(
    text="Teste de voz isolado",
    speaker_wav="/home/n8n/files/voice_sample.wav",
    language="pt",
    file_path="/tmp/teste_tts.wav"
)
print("✅ TTS funcionando!")
EOF

# Baixar o áudio de teste
scp root@31.97.142.45:/tmp/teste_tts.wav .
```

---

### **11. Verificar Dependências Instaladas**
```bash
sudo -u n8n /opt/tts-env/bin/pip list | grep -E "torch|TTS|transformers|Pillow|moviepy"
```

**Versões esperadas:**
```
torch            2.1.0
torchaudio       2.1.0
TTS              0.22.0
transformers     4.33.0
Pillow           9.5.0
moviepy          1.0.3
```

---

### **12. Monitorar Recursos do Sistema**
```bash
# Ver uso de CPU e memória em tempo real
htop

# Ver uso de disco
df -h

# Ver uso de memória
free -h

# Ver processos Python
ps aux | grep python
```

---

### **13. Testar com Texto Longo (30+ palavras)**
```bash
curl -X POST http://31.97.142.45:5005/create-video \
  -H "Content-Type: application/json" \
  -d '{"id": "teste_longo", "text": "Bem vindo ao sistema de automação de vídeos profissional. Este sistema utiliza inteligência artificial para clonar sua voz com alta qualidade usando o modelo XTTS_v2. As imagens são processadas automaticamente e sincronizadas com o áudio gerado. O formato do vídeo é otimizado para redes sociais em formato vertical de reels."}'
```

---

### **14. Limpar Cache e Modelos (Se necessário)**
```bash
# Limpar cache do pip
sudo -u n8n rm -rf /home/n8n/.cache/pip

# Limpar modelos TTS baixados (vai baixar novamente quando usar)
sudo -u n8n rm -rf /home/n8n/.local/share/tts

# Limpar modelos Whisper
sudo -u n8n rm -rf /home/n8n/.cache/whisper
```

---

### **15. Troubleshooting Rápido**

#### **Servidor não responde:**
```bash
sudo systemctl status video-automation
sudo journalctl -u video-automation -n 20
```

#### **Porta em uso:**
```bash
sudo netstat -tlnp | grep 5005
sudo fuser -k 5005/tcp
sudo systemctl restart video-automation
```

#### **Vídeo não foi criado:**
```bash
# Ver logs completos
sudo journalctl -u video-automation -n 100

# Verificar permissões
ls -la /home/n8n/files/videos/
ls -la /home/n8n/files/imagens/
```

#### **Erro de importação:**
```bash
# Testar imports manualmente
sudo -u n8n /opt/tts-env/bin/python3 -c "from TTS.api import TTS; print('TTS OK')"
sudo -u n8n /opt/tts-env/bin/python3 -c "from moviepy.editor import *; print('MoviePy OK')"
sudo -u n8n /opt/tts-env/bin/python3 -c "import whisper_timestamped; print('Whisper OK')"
```

---

### **16. Integração com N8n**

**Endpoint:** `http://31.97.142.45:5005/create-video`

**Método:** `POST`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "id": "video_{{ $json.id }}",
  "text": "{{ $json.texto }}"
}
```

**⚠️ IMPORTANTE:**
- O texto deve estar em UMA LINHA (sem quebras `\n`)
- As imagens devem estar em `/files/imagens/` ANTES da requisição
- O ID deve ser único

---

### **17. Exemplo Completo de Workflow**

```bash
# 1. Fazer upload de imagens (do N8n para /files/imagens/)
# 2. Chamar API de criação:

curl -X POST http://31.97.142.45:5005/create-video \
  -H "Content-Type: application/json" \
  -d '{"id": "prod001", "text": "Seu texto de produção aqui"}'

# 3. Aguardar ~1-2 minutos

# 4. Verificar se terminou:
curl http://31.97.142.45:5005/status/prod001

# 5. Quando status="completed", baixar o vídeo:
# No N8n: GET http://31.97.142.45:5005/download/videos/video_prod001.mp4
```

---

## 📊 **Tempo de Processamento Esperado:**

| Etapa | Tempo |
|-------|-------|
| Geração de áudio (XTTS_v2) | ~30-60s |
| Criação do vídeo (MoviePy) | ~30-60s |
| **TOTAL** | **~1-2 minutos** |

---

## ✅ **Checklist de Funcionamento:**

- [ ] Servidor responde em `/health`
- [ ] Consegue criar vídeo via API
- [ ] Vídeo aparece em `/home/n8n/files/videos/`
- [ ] Qualidade da voz está boa (XTTS_v2)
- [ ] Imagens processam corretamente (Pillow 9.5.0)
- [ ] Formato Reels correto (1080x1920)
- [ ] N8n consegue fazer upload de imagens
- [ ] N8n consegue baixar vídeo pronto

---

**Use este arquivo como referência para testes e troubleshooting!** 📚

