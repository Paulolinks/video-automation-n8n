# 📝 Changelog - Video Automation N8n

## [2.0.0] - 2025-10-08

### 🎉 Versão 2.0 - Grande Atualização

Esta versão adiciona recursos avançados mantendo total compatibilidade com a Versão 1.

### ✨ Novos Recursos

#### 🌐 API REST Completa
- **Servidor Flask** na porta 5005
- Endpoints para geração de áudio e vídeo
- Endpoint para listar fontes disponíveis
- Validação de parâmetros
- Tratamento de erros robusto

#### 🖥️ Interface Web
- **Interface moderna** na porta 5006
- Configuração visual de:
  - Fonte padrão (9 opções)
  - Tipo de vídeo (imagens/vídeos)
  - Qualidade de renderização
  - Tamanho e cor das legendas
- Preview de configurações em tempo real
- Salva e carrega configurações automaticamente

#### 🎨 Sistema de Fontes
- **9 fontes personalizadas** disponíveis
- Seleção via API ou interface web
- Fontes instaladas automaticamente
- Lista de fontes via endpoint `/fonts`

#### 🎬 Suporte a Vídeos
- **Novo script**: `make_video_with_videos.py`
- Criação com clipes de vídeo além de imagens
- Suporte para MP4, AVI, MOV, MKV
- Mesmo sistema de legendas

#### ⚡ Otimização de Memória
- **Versão otimizada**: `make_video_optimized.py`
- Gerenciamento inteligente de memória com `gc.collect()`
- Processamento em lotes
- Ideal para VPS com 4-8GB RAM

#### 🚀 Instalação Automática
- **Script completo**: `install_vps.sh`
- Instala todas as dependências
- Configura serviços systemd
- Configura firewall automaticamente
- Tempo: ~20-25 minutos

#### 🔄 Integração N8n
- **Workflow de exemplo** incluído
- Fluxo completo pré-configurado
- Nós HTTP Request prontos
- Documentação de uso

### 📁 Novos Arquivos

```
files/
├── server.py                    # API REST principal
├── web_interface.py             # Interface web
├── make_video_optimized.py      # Versão otimizada
├── make_video_with_videos.py    # Suporte para vídeos
├── install_vps.sh               # Instalação automática
├── n8n_example_workflow.json    # Workflow N8n
├── templates/
│   └── index.html               # Interface web
├── README.md                    # Documentação principal
├── VERSION_GUIDE.md             # Guia de versões
└── CHANGELOG.md                 # Este arquivo
```

### 🔧 Melhorias

#### Scripts Originais (V1)
- `make_video.py`: Aceita fonte como parâmetro
- `server.py`: Expandido com novos endpoints
- `.gitignore`: Otimizado para preservar arquivos importantes

#### Documentação
- README completo com comparação de versões
- Guia detalhado de escolha de versão
- Exemplos de uso para ambas versões
- Instruções de instalação passo a passo

### 🔒 Arquivos Preservados

Os seguintes arquivos foram mantidos e **não serão deletados**:
- ✅ `voice_sample.wav` - Sua amostra de voz
- ✅ `final_video.mp4` - Vídeo de exemplo

### 🎯 Compatibilidade

- ✅ **100% compatível** com Versão 1
- ✅ Ambas versões podem coexistir
- ✅ Scripts V1 funcionam sem alteração
- ✅ V2 usa scripts V1 internamente

### 📊 Estatísticas

- **Arquivos adicionados**: 8 novos arquivos
- **Linhas de código**: +1.556 linhas
- **Novos endpoints**: 3 endpoints API
- **Fontes disponíveis**: 9 fontes
- **Documentação**: 3 novos arquivos MD

### 🚀 Como Atualizar

#### Opção 1: Clonar novamente
```bash
git clone https://github.com/Paulolinks/video-automation-n8n.git
cd video-automation-n8n/files
chmod +x install_vps.sh
sudo ./install_vps.sh
```

#### Opção 2: Pull no repositório existente
```bash
cd video-automation-n8n
git pull origin master
cd files
chmod +x install_vps.sh
sudo ./install_vps.sh
```

### 🧪 Testado Em

- ✅ Ubuntu 20.04 / 22.04
- ✅ Debian 11
- ✅ VPS Hostinger KVM2 (8GB RAM, 2 CPU)
- ✅ Python 3.9, 3.10, 3.11

### 📝 Notas de Migração

1. **Não há breaking changes** - Tudo da V1 continua funcionando
2. **Instalação opcional** - Pode usar V2 quando quiser
3. **Configurações** - V2 usa `config.json` para configurações
4. **Portas** - V2 usa portas 5005 (API) e 5006 (Web)

### 🐛 Correções

- Correção no tratamento de nomes de arquivo com `\n`
- Melhoria no gerenciamento de memória
- Validação de fontes disponíveis
- Tratamento de erros mais robusto

### 🔮 Próximas Versões (Planejado)

- [ ] Cache de áudios gerados
- [ ] Processamento em background
- [ ] Múltiplas amostras de voz
- [ ] Templates de vídeo personalizados
- [ ] Analytics e estatísticas
- [ ] Webhooks para notificações
- [ ] Suporte a múltiplos idiomas

---

## [1.0.0] - 2024

### Versão Original

- Criação de vídeos com imagens
- TTS com voz clonada
- Legendas automáticas
- Scripts Python diretos
- Integração básica com N8n

---

**Para mais informações**, consulte:
- [README.md](README.md) - Documentação principal
- [VERSION_GUIDE.md](VERSION_GUIDE.md) - Guia de escolha de versão
