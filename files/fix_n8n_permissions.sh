#!/bin/bash
# Script para corrigir permissões do N8n

echo "🔧 CORRIGINDO PERMISSÕES DO N8N..."
echo ""

# Cria pastas se não existirem
echo "📁 Criando pastas para N8n..."
sudo mkdir -p /files/imagens
sudo mkdir -p /files/videos
sudo mkdir -p /files/fonts

# Configura permissões
echo "🔐 Configurando permissões..."
sudo chown -R n8n:n8n /files
sudo chmod 755 /files/imagens
sudo chmod 755 /files/videos
sudo chmod 755 /files/fonts

# Cria link simbólico se necessário
echo "🔗 Criando links simbólicos..."
sudo ln -sf /files /home/n8n/files 2>/dev/null || echo "Link já existe"

echo ""
echo "✅ PERMISSÕES CORRIGIDAS!"
echo "📂 N8n pode agora escrever em:"
echo "  - /files/imagens/"
echo "  - /files/videos/"
echo "  - /files/fonts/"
echo ""
echo "🧪 Teste no N8n:"
echo "  File Path: /files/imagens/teste.jpg"
echo ""
