# ⚠️ PROBLEMA: Serviços Duplicados no VPS

## 🔍 **Se você encontrar o erro "Address already in use"**

Isso acontece quando há **múltiplos serviços** tentando usar a porta 5005.

---

## 📋 **Como Identificar:**

```bash
# 1. Ver todos os serviços relacionados
sudo systemctl list-units | grep -E "video|automation|tts|flask|server"

# 2. Ver processos Python
ps aux | grep python

# 3. Ver o que está na porta 5005
sudo lsof -i :5005
sudo netstat -tlnp | grep 5005
```

---

## 🔧 **Como Corrigir:**

### **Se encontrar serviços duplicados (ex: `tts-video.service`):**

```bash
# 1. Listar TODOS os serviços do sistema
sudo systemctl list-unit-files | grep -E "video|automation|tts"

# 2. Parar e desabilitar serviços antigos/duplicados
sudo systemctl stop tts-video.service
sudo systemctl disable tts-video.service

sudo systemctl stop video-creator.service
sudo systemctl disable video-creator.service

sudo systemctl stop video-web.service
sudo systemctl disable video-web.service

# 3. Deletar arquivos de serviço antigos
sudo rm -f /etc/systemd/system/tts-video.service
sudo rm -f /etc/systemd/system/video-creator.service
sudo rm -f /etc/systemd/system/video-web.service

# 4. Recarregar systemd
sudo systemctl daemon-reload

# 5. Matar TODOS os processos Python
sudo pkill -9 python3
sudo fuser -k 5005/tcp

# 6. Iniciar APENAS o serviço correto
sudo systemctl start video-automation

# 7. Verificar
curl http://localhost:5005/health
```

---

## 🚨 **Serviço Correto:**

**Nome:** `video-automation.service`

**Localização:** `/etc/systemd/system/video-automation.service`

**Comando:** `/opt/tts-env/bin/python3 /home/n8n/files/server.py`

**Porta:** `5005`

---

## 🔍 **Verificação Final:**

```bash
# Deve mostrar APENAS video-automation.service
sudo systemctl list-units --type=service --state=running | grep video

# Deve mostrar APENAS um processo Python na porta 5005
sudo lsof -i :5005
```

**Se aparecer mais de um serviço ou processo, repita os passos de limpeza acima!**

---

## 💡 **Dica: Após Limpar:**

Se mesmo assim continuar dando problema:

```bash
# REINICIAR O VPS
sudo reboot

# Aguardar 1 minuto, reconectar e verificar:
curl http://31.97.142.45:5005/health
```

**O reboot mata TUDO e inicia limpo!**

---

## ✅ **Prevenção:**

**NÃO execute** `server.py` manualmente fora do systemd:
```bash
# ❌ NÃO FAÇA:
python3 /home/n8n/files/server.py

# ✅ FAÇA:
sudo systemctl start video-automation
```

**Sempre use o systemd para gerenciar o servidor!**

