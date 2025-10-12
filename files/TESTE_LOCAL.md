# 🧪 TESTE LOCAL - VIDEO AUTOMATION

## 📋 **PRÉ-REQUISITOS**

1. **Python 3.11** instalado no Windows
   - Download: https://www.python.org/downloads/
   - ✅ Marque "Add Python to PATH" durante a instalação

2. **Arquivos necessários**:
   - ✅ `voice_sample.wav` (já presente)
   - ✅ `server.py` e `create_video.py`
   - ✅ Pasta `imagens` com algumas imagens para teste

---

## 🚀 **INSTALAÇÃO LOCAL**

### **Passo 1: Instalar dependências**
```cmd
# Execute o script de instalação
python setup_local.py
```

**O que faz:**
- ✅ Cria ambiente virtual Python
- ✅ Instala Flask, PyTorch, TTS, MoviePy, Whisper
- ✅ Testa todas as importações
- ✅ Cria pastas necessárias

---

## 🧪 **TESTES LOCAIS**

### **Teste 1: Teste Direto (Sem Servidor)**
```cmd
# Testa criação de vídeo diretamente
python test_video.py
```

**Resultado esperado:**
- ✅ Arquivo `videos/video_teste_local_001.mp4` criado
- ✅ Áudio com voice cloning
- ✅ Legendas automáticas

### **Teste 2: Teste Manual**
```cmd
# Teste direto do create_video.py
venv\Scripts\python.exe create_video.py "Seu texto aqui" "teste_manual"
```

### **Teste 3: Servidor Completo**
```cmd
# Inicia servidor Flask
venv\Scripts\python.exe server.py
```

**Em outro terminal:**
```cmd
# Teste via API
curl http://localhost:5005/health
curl -X POST http://localhost:5005/create-video -H "Content-Type: application/json" -d "{\"id\": \"teste_api\", \"text\": \"Teste via API local\"}"
```

---

## 🔧 **SOLUÇÃO DE PROBLEMAS**

### **Erro: "cannot import name 'BeamSearchScorer'"**
```cmd
# Reinstalar TTS com versão específica
venv\Scripts\activate.bat
pip uninstall TTS -y
pip install TTS==0.22.0
```

### **Erro: "voice_sample.wav not found"**
- ✅ Certifique-se que o arquivo está na pasta `files/`
- ✅ Verifique se o arquivo não está corrompido

### **Erro: "No images found"**
- ✅ Adicione algumas imagens na pasta `imagens/`
- ✅ Formatos suportados: .jpg, .jpeg, .png

### **Erro: "FFmpeg not found"**
```cmd
# Instalar FFmpeg via pip
pip install imageio-ffmpeg
```

---

## 📊 **VERIFICAÇÃO DE FUNCIONAMENTO**

### **✅ Checklist de Sucesso:**
- [ ] Ambiente virtual criado
- [ ] Todas as dependências instaladas
- [ ] Importações funcionando
- [ ] Servidor iniciando sem erro
- [ ] Vídeo sendo criado na pasta `videos/`
- [ ] Áudio com voice cloning funcionando
- [ ] Legendas sendo geradas

### **📁 Estrutura de Pastas:**
```
files/
├── venv/                 # Ambiente virtual
├── imagens/              # Imagens para vídeo
├── videos/               # Vídeos gerados
├── fonts/                # Fontes para legendas
├── voice_sample.wav      # Sample de voz
├── server.py             # Servidor Flask
├── create_video.py       # Gerador de vídeo
├── setup_local.bat       # Instalador
├── test_local.bat        # Teste servidor
└── quick_test.bat        # Teste rápido
```

---

## 🎯 **PRÓXIMOS PASSOS**

1. **✅ Teste local funcionando**
2. **🚀 Aplicar correções no VPS**
3. **📡 Configurar N8n**
4. **🎬 Produção em massa**

---

## 💡 **DICAS**

- **Primeiro teste**: Use `quick_test.bat` (mais rápido)
- **Teste completo**: Use `test_local.bat` (servidor + API)
- **Debug**: Execute `create_video.py` manualmente para ver logs
- **Performance**: Primeira execução é mais lenta (download de modelos)
