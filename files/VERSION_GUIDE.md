# 📖 Guia de Versões

## 🤔 Qual versão devo usar?

### 🔹 Use a **Versão 1** se você:
- Prefere executar scripts manualmente
- Quer controle total sobre cada etapa
- Não precisa de API REST
- Tem um VPS simples ou está testando localmente
- Gosta de simplicidade e comandos diretos

**Exemplo de uso:**
```bash
python3 make_video.py "Frase motivacional" 001
```

---

### 🚀 Use a **Versão 2** se você:
- Quer automação completa com N8n
- Precisa de uma API REST
- Quer uma interface web para configurar
- Deseja escolher diferentes fontes
- Precisa criar vídeos com vídeos (não só imagens)
- Quer otimização de memória para VPS
- Planeja escalar a produção

**Exemplo de uso:**
```bash
curl -X POST http://seu-vps:5005/generate-video \
  -H "Content-Type: application/json" \
  -d '{"frase": "Frase aqui", "id": "001", "font": "Anton"}'
```

---

## 📋 Comparação Detalhada

### Versão 1 (Original)
**Prós:**
- ✅ Simples e direto
- ✅ Fácil de entender
- ✅ Funciona perfeitamente
- ✅ Menos dependências

**Contras:**
- ❌ Sem API
- ❌ Sem interface web
- ❌ Fonte fixa no código
- ❌ Apenas imagens

**Arquivos principais:**
- `make_video.py`
- `add_subtitles.py`
- `tts_audio_highquality.py`
- `run_tts.sh` / `run_video.sh`

---

### Versão 2 (Melhorada)
**Prós:**
- ✅ API REST completa
- ✅ Interface web moderna
- ✅ Múltiplas fontes
- ✅ Suporte a vídeos
- ✅ Otimização de memória
- ✅ Instalação automática
- ✅ Workflow N8n pronto

**Contras:**
- ❌ Mais complexa
- ❌ Mais dependências
- ❌ Requer configuração de serviços

**Arquivos principais:**
- `server.py` (API)
- `web_interface.py` (Interface)
- `make_video_optimized.py`
- `make_video_with_videos.py`
- `install_vps.sh`

---

## 🔄 Migração de V1 para V2

Se você está usando V1 e quer testar V2, não precisa mudar nada!

### Passo 1: Mantenha V1 funcionando
Seus scripts da V1 continuam funcionando normalmente.

### Passo 2: Instale V2 em paralelo
```bash
cd /home/n8n/files
chmod +x install_vps.sh
sudo ./install_vps.sh
```

### Passo 3: Teste V2
```bash
# Teste a API
curl http://localhost:5005/health

# Acesse a interface
http://seu-ip:5006
```

### Passo 4: Use ambas!
- Continue usando V1 para testes rápidos
- Use V2 para automação com N8n

---

## 🎯 Casos de Uso

### Caso 1: Criação Manual Rápida
**Versão recomendada: V1**
```bash
python3 tts_audio_highquality.py "Texto" 001
python3 make_video.py "Texto" 001
```

### Caso 2: Automação com N8n
**Versão recomendada: V2**
- Use o workflow `n8n_example_workflow.json`
- Configure os HTTP Request nodes
- Deixe o N8n fazer tudo automaticamente

### Caso 3: Produção em Larga Escala
**Versão recomendada: V2**
- API REST para múltiplas requisições
- Interface web para gerenciar
- Otimização de memória

### Caso 4: Testes e Aprendizado
**Versão recomendada: V1**
- Scripts simples para entender o processo
- Fácil de modificar e experimentar

---

## 📝 Exemplos Práticos

### Exemplo 1: Vídeo Simples (V1)
```bash
# Passo 1: Criar áudio
python3 tts_audio_highquality.py "Acredite em você!" 001

# Passo 2: Criar vídeo
python3 make_video.py "Acredite em você!" 001

# Resultado: /home/n8n/files/video_001.mp4
```

### Exemplo 2: Vídeo via API (V2)
```bash
# Tudo em uma chamada
curl -X POST http://localhost:5005/generate-video \
  -H "Content-Type: application/json" \
  -d '{
    "frase": "Acredite em você!",
    "id": "001",
    "font": "Active_Heart",
    "type": "images"
  }'

# Resultado: /home/n8n/files/video_001.mp4
```

### Exemplo 3: Vídeo com Vídeos (V2 Only)
```bash
curl -X POST http://localhost:5005/generate-video \
  -H "Content-Type: application/json" \
  -d '{
    "frase": "Acredite em você!",
    "id": "002",
    "font": "Anton",
    "type": "videos"
  }'
```

---

## 🔧 Configuração de Fontes

### V1: Editar no código
```python
# Em make_video.py, linha 16
FONT_NAME = "Anton"  # Mude aqui
```

### V2: Via API ou Interface Web
```bash
# Via API
curl -X POST http://localhost:5005/generate-video \
  -d '{"font": "Active_Heart", ...}'

# Via Interface Web
Acesse http://seu-ip:5006 e escolha na lista
```

---

## 🐛 Resolução de Problemas

### Problema: V1 e V2 conflitam?
**Resposta:** Não! Elas podem coexistir:
- V1 usa scripts diretamente
- V2 usa serviços systemd (portas 5005 e 5006)

### Problema: Como sei qual versão está rodando?
```bash
# V1: Você executa manualmente
python3 make_video.py ...

# V2: Serviços systemd
sudo systemctl status video-creator
```

### Problema: Posso usar scripts V1 com API V2?
**Resposta:** Sim! A V2 chama os scripts V1 internamente.

---

## 💡 Recomendações Finais

1. **Comece com V1** para entender como funciona
2. **Migre para V2** quando precisar de automação
3. **Mantenha ambas** para flexibilidade
4. **Use V2 para produção**, V1 para testes

---

**🎬 Boas criações de vídeos!**
