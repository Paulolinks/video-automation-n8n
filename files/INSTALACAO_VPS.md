# 🚀 Guia de Instalação no VPS

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter:
- ✅ Acesso SSH ao seu VPS
- ✅ VPS com Ubuntu 20.04+ ou Debian 11+
- ✅ Mínimo 4GB RAM (recomendado 8GB)
- ✅ Python 3.9 ou superior
- ✅ Acesso root ou sudo

## 🎯 Instalação Rápida (5 minutos de setup + 20 minutos de instalação)

### Passo 1: Conectar ao VPS

```bash
ssh usuario@seu_vps_ip
```

Ou se usar chave SSH:
```bash
ssh -i sua_chave.pem usuario@seu_vps_ip
```

### Passo 2: Clonar o Repositório

```bash
cd /home
git clone https://github.com/Paulolinks/video-automation-n8n.git
cd video-automation-n8n/files
```

### Passo 3: Executar Instalação

```bash
# Tornar o script executável
chmod +x install_vps.sh

# Executar instalação
sudo ./install_vps.sh
```

**⏱️ Tempo estimado**: 20-25 minutos

O script irá:
1. Atualizar o sistema
2. Instalar Python e dependências
3. Instalar FFmpeg e ImageMagick
4. Criar ambiente virtual Python
5. Instalar bibliotecas Python (MoviePy, Whisper, TTS, etc.)
6. Instalar as fontes personalizadas
7. Criar serviços systemd
8. Configurar firewall
9. Iniciar os serviços

### Passo 4: Verificar Instalação

```bash
# Verificar se os serviços estão rodando
sudo systemctl status video-creator
sudo systemctl status video-web

# Testar API
curl http://localhost:5005/health
curl http://localhost:5005/fonts

# Verificar logs
sudo journalctl -u video-creator -n 50
sudo journalctl -u video-web -n 50
```

### Passo 5: Acessar Interface Web

Abra no navegador:
```
http://SEU_VPS_IP:5006
```

## 📁 Estrutura Após Instalação

```
/home/n8n/files/
├── server.py                    # API (porta 5005)
├── web_interface.py             # Interface Web (porta 5006)
├── make_video.py                # Scripts V1 e V2
├── make_video_optimized.py
├── make_video_with_videos.py
├── tts_audio_highquality.py
├── config.json                  # Configurações
├── fonts/                       # 9 fontes instaladas
├── templates/                   # Interface web
├── imagens/                     # Coloque imagens aqui
├── videos/                      # Coloque vídeos aqui
└── voice_sample.wav             # SUA VOZ (importante!)

/opt/tts-env/                    # Ambiente virtual Python
/etc/systemd/system/
├── video-creator.service        # Serviço API
└── video-web.service            # Serviço Web
```

## 🔑 Configurações Importantes

### 1. Adicionar Sua Amostra de Voz

**IMPORTANTE**: Coloque sua amostra de voz no VPS!

```bash
# Do seu computador, envie o arquivo
scp voice_sample.wav usuario@seu_vps_ip:/home/n8n/files/

# Ou use WinSCP se preferir interface gráfica
```

Requisitos do arquivo:
- Formato: WAV
- Duração: 10-30 segundos
- Qualidade: Melhor qualidade possível
- Conteúdo: Fale frases variadas com emoção natural

### 2. Adicionar Imagens/Vídeos

```bash
# Fazer upload de imagens
scp imagem1.jpg imagem2.png usuario@seu_vps_ip:/home/n8n/files/imagens/

# Fazer upload de vídeos
scp video1.mp4 video2.mp4 usuario@seu_vps_ip:/home/n8n/files/videos/
```

### 3. Configurar N8n

No seu N8n, importe o workflow:
```bash
# O arquivo está em:
files/n8n_example_workflow.json
```

Configure os HTTP Request nodes com:
- URL da API: `http://SEU_VPS_IP:5005`
- Endpoints disponíveis

## 🔥 Configuração do Firewall

Se o firewall estiver bloqueando, libere as portas:

```bash
# UFW (Ubuntu/Debian)
sudo ufw allow 5005/tcp
sudo ufw allow 5006/tcp
sudo ufw reload

# Firewalld (CentOS/RHEL)
sudo firewall-cmd --permanent --add-port=5005/tcp
sudo firewall-cmd --permanent --add-port=5006/tcp
sudo firewall-cmd --reload

# iptables
sudo iptables -A INPUT -p tcp --dport 5005 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5006 -j ACCEPT
sudo iptables-save
```

**No painel da Hostinger**: Verifique se as portas estão liberadas no firewall do painel.

## 🧪 Testando o Sistema

### Teste 1: Gerar Áudio

```bash
curl -X POST http://localhost:5005/generate-audio \
  -H "Content-Type: application/json" \
  -d '{
    "frase": "Este é um teste de áudio",
    "id": "teste001"
  }'
```

### Teste 2: Gerar Vídeo

```bash
curl -X POST http://localhost:5005/generate-video \
  -H "Content-Type: application/json" \
  -d '{
    "frase": "Este é um teste de vídeo",
    "id": "teste002",
    "font": "Anton",
    "type": "images"
  }'
```

### Teste 3: Listar Fontes

```bash
curl http://localhost:5005/fonts
```

## 🔧 Comandos Úteis

### Gerenciar Serviços

```bash
# Verificar status
sudo systemctl status video-creator
sudo systemctl status video-web

# Parar serviços
sudo systemctl stop video-creator
sudo systemctl stop video-web

# Iniciar serviços
sudo systemctl start video-creator
sudo systemctl start video-web

# Reiniciar serviços
sudo systemctl restart video-creator
sudo systemctl restart video-web

# Ver logs em tempo real
sudo journalctl -u video-creator -f
sudo journalctl -u video-web -f
```

### Verificar Recursos

```bash
# Uso de memória
free -h

# Uso de CPU
top

# Uso de disco
df -h

# Processos Python
ps aux | grep python
```

### Limpar Arquivos Temporários

```bash
# Limpar vídeos gerados
cd /home/n8n/files
rm -f audio_*.wav video_*.mp4 subs_*.json temp-*.m4a

# Manter apenas voice_sample.wav e final_video.mp4
```

## 🐛 Solução de Problemas

### Problema 1: Serviço não inicia

```bash
# Ver erro específico
sudo journalctl -u video-creator -n 100 --no-pager

# Verificar permissões
ls -la /home/n8n/files/
sudo chown -R n8n:n8n /home/n8n/files/

# Testar script manualmente
sudo -u n8n /opt/tts-env/bin/python3 /home/n8n/files/server.py
```

### Problema 2: Erro de memória

```bash
# Use a versão otimizada
# No server.py, troque:
# make_video.py -> make_video_optimized.py

# Ou reduza qualidade na interface web
```

### Problema 3: Fontes não aparecem

```bash
# Reinstalar fontes
sudo cp /home/n8n/files/fonts/*.ttf /usr/share/fonts/truetype/
sudo fc-cache -fv

# Verificar fontes instaladas
fc-list | grep -i anton
```

### Problema 4: Erro no TTS

```bash
# Verificar se voice_sample.wav existe
ls -lh /home/n8n/files/voice_sample.wav

# Testar TTS manualmente
sudo -u n8n /opt/tts-env/bin/python3 /home/n8n/files/tts_audio_highquality.py "Teste" 999
```

### Problema 5: API não responde

```bash
# Verificar se porta está aberta
sudo netstat -tulpn | grep 5005

# Testar localmente
curl http://localhost:5005/health

# Ver logs de erro
sudo journalctl -u video-creator -n 50
```

## 📊 Monitoramento

### Script de Monitoramento Simples

Crie um arquivo `monitor.sh`:

```bash
#!/bin/bash
echo "=== Status dos Serviços ==="
systemctl is-active video-creator
systemctl is-active video-web

echo -e "\n=== Uso de Recursos ==="
free -h | grep Mem
df -h | grep sda1

echo -e "\n=== Últimos Logs ==="
journalctl -u video-creator -n 5 --no-pager

echo -e "\n=== Teste de API ==="
curl -s http://localhost:5005/health
```

Execute:
```bash
chmod +x monitor.sh
./monitor.sh
```

## 🔄 Atualização do Sistema

### Atualizar para Versão Nova

```bash
cd /home/n8n/video-automation-n8n
git pull origin master

# Reiniciar serviços
sudo systemctl restart video-creator
sudo systemctl restart video-web
```

### Reinstalar Dependências

```bash
sudo -u n8n /opt/tts-env/bin/pip install --upgrade \
  moviepy whisper-timestamped TTS torch torchaudio flask pillow
```

## 💡 Dicas de Performance

### 1. Para VPS com 4GB RAM
- Use `make_video_optimized.py`
- Configure quality como "low" ou "medium"
- Processe menos imagens por vez

### 2. Para VPS com 8GB RAM
- Pode usar todas as versões
- Configure quality como "medium" ou "high"
- Processe quantas imagens quiser

### 3. Otimizações Gerais
- Mantenha imagens em resolução razoável (não precisa 4K)
- Use vídeos curtos (10-30 segundos)
- Limpe arquivos temporários regularmente

## 📞 Suporte

Se algo não funcionar:

1. **Verifique os logs**: `sudo journalctl -u video-creator -f`
2. **Teste manualmente**: Execute os scripts Python diretamente
3. **Verifique recursos**: `free -h`, `df -h`
4. **Reinstale**: Em último caso, rode `install_vps.sh` novamente

## ✅ Checklist Final

Após instalação, verifique:

- [ ] Serviços rodando: `systemctl status video-creator video-web`
- [ ] API respondendo: `curl http://localhost:5005/health`
- [ ] Interface acessível: `http://SEU_IP:5006`
- [ ] Fontes instaladas: `curl http://localhost:5005/fonts`
- [ ] Voice sample no lugar: `ls /home/n8n/files/voice_sample.wav`
- [ ] Imagens/vídeos adicionados
- [ ] N8n configurado e testado
- [ ] Firewall liberado
- [ ] Primeiro vídeo teste criado

---

**🎬 Seu sistema está pronto para criar vídeos automaticamente!**

Próximo passo: Configure seu workflow no N8n e comece a produzir conteúdo!
