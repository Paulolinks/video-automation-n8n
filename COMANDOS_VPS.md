# 🚀 COMANDOS PARA CORRIGIR E TESTAR NO VPS

## ⚡ CORREÇÃO RÁPIDA (Aplicar no VPS que já está instalado)

```bash
# 1. Corrigir PyTorch e Transformers (para XTTS_v2 funcionar)
sudo -u n8n /opt/tts-env/bin/pip uninstall -y torch torchaudio transformers
sudo -u n8n /opt/tts-env/bin/pip install torch==2.1.0 torchaudio==2.1.0
sudo -u n8n /opt/tts-env/bin/pip install transformers==4.33.0

# 2. Reinstalar TTS
sudo -u n8n /opt/tts-env/bin/pip install --force-reinstall --no-deps TTS
sudo -u n8n /opt/tts-env/bin/pip install TTS

# 3. Reiniciar serviço
sudo systemctl restart video-automation

# 4. Aguardar 5 segundos
sleep 5

# 5. Verificar se está rodando
sudo systemctl status video-automation

# 6. Testar saúde do servidor
curl http://localhost:5005/health
```

---

## 🎬 TESTAR CRIAÇÃO DE VÍDEO

```bash
# Teste com texto simples (UMA LINHA, SEM QUEBRAS)
curl -X POST http://31.97.142.45:5005/create-video \
  -H "Content-Type: application/json" \
  -d '{"id": "teste_voz", "text": "Este é um teste de qualidade de voz com XTTS_v2 no VPS. A clonagem deve estar muito melhor agora."}'

# Verificar status do processamento
curl http://31.97.142.45:5005/status/teste_voz

# Ver logs em tempo real
sudo journalctl -u video-automation -f
```

---

## 🔄 REINSTALAÇÃO COMPLETA (Se preferir começar do zero)

```bash
# 1. Limpar instalação anterior
sudo systemctl stop video-automation
sudo rm -rf /opt/tts-env
sudo rm -rf /home/n8n/files/*

# 2. Reinstalar tudo com a versão nova do GitHub
sudo curl -sSL https://raw.githubusercontent.com/Paulolinks/video-automation-n8n/master/files/quick_install.sh | bash
```

---

## 📊 COMANDOS ÚTEIS

```bash
# Ver logs do servidor
sudo journalctl -u video-automation -n 50

# Ver logs em tempo real
sudo journalctl -u video-automation -f

# Verificar status do serviço
sudo systemctl status video-automation

# Reiniciar serviço
sudo systemctl restart video-automation

# Parar serviço
sudo systemctl stop video-automation

# Ver processos rodando
ps aux | grep python

# Verificar porta 5005
netstat -tlnp | grep 5005

# Listar vídeos criados
ls -lh /home/n8n/files/videos/

# Baixar vídeo (substitua SEU_IP pelo IP do VPS)
scp root@SEU_IP:/home/n8n/files/videos/video_teste_voz.mp4 .
```

---

## ⚠️ IMPORTANTE

**Para N8n funcionar corretamente:**
1. Use texto em UMA ÚNICA LINHA (sem quebras `\n`)
2. O ID deve ser único para cada vídeo
3. As imagens devem estar em `/files/imagens/` ANTES da requisição

**Exemplo de requisição CORRETA:**
```json
{
  "id": "video001",
  "text": "Seu texto completo aqui em uma única linha sem quebras de linha."
}
```

**Exemplo ERRADO (não faça isso):**
```json
{
  "id": "video001",
  "text": "Primeira linha
Segunda linha
Terceira linha"
}
```

---

## 🎯 PRÓXIMOS PASSOS

1. Execute a correção rápida acima
2. Teste a criação de vídeo
3. Ouça o áudio e verifique a qualidade
4. Se estiver bom, configure o N8n para usar a API
5. Se ainda não estiver bom, me avise qual é o problema específico

**A qualidade da voz com XTTS_v2 deve estar MUITO melhor que o teste local!** 🎤✨

