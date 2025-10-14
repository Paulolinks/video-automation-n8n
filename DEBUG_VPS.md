# 🔍 DEBUG - SERVIDOR NÃO INICIA

Execute estes comandos para descobrir o erro:

```bash
# 1. Ver o erro completo do serviço
sudo journalctl -u video-automation -n 100 --no-pager

# 2. Tentar rodar manualmente para ver o erro
sudo -u n8n /opt/tts-env/bin/python3 /home/n8n/files/server.py

# 3. Verificar se os arquivos existem
ls -la /home/n8n/files/

# 4. Verificar permissões
ls -la /home/n8n/files/server.py
ls -la /home/n8n/files/create_video.py

# 5. Testar import do TTS
sudo -u n8n /opt/tts-env/bin/python3 -c "from TTS.api import TTS; print('TTS OK')"

# 6. Verificar versões instaladas
sudo -u n8n /opt/tts-env/bin/pip list | grep -E "torch|TTS|transformers"
```

---

## 🎯 COPIE E EXECUTE NO VPS

**Execute o comando 2 primeiro** (rodar manualmente):
```bash
sudo -u n8n /opt/tts-env/bin/python3 /home/n8n/files/server.py
```

**Isso vai mostrar o erro exato!** Me envie a saída completa.

