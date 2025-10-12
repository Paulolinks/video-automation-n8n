#!/usr/bin/env python3
"""
========================================
VIDEO AUTOMATION - TESTE DIRETO
========================================
Script para testar criação de vídeo diretamente
sem servidor Flask
========================================
"""

import os
import sys
import platform

def get_python_cmd():
    """Retorna comando Python baseado no sistema"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\python.exe"
    else:
        return "venv/bin/python"

def check_setup():
    """Verifica se setup foi feito"""
    print("🔍 Verificando setup...")
    
    if not os.path.exists("venv"):
        print("❌ Ambiente virtual não encontrado!")
        print("   Execute primeiro: python setup_local.py")
        return False
    
    if not os.path.exists("voice_sample.wav"):
        print("❌ voice_sample.wav não encontrado!")
        return False
    
    if not os.path.exists("imagens"):
        print("❌ Pasta imagens não encontrada!")
        return False
    
    # Verifica se há imagens
    image_files = [f for f in os.listdir("imagens") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print("❌ Nenhuma imagem encontrada na pasta imagens/")
        print("   Adicione algumas imagens (.jpg, .png) na pasta imagens/")
        return False
    
    print(f"✅ Setup OK - {len(image_files)} imagens encontradas")
    return True

def test_create_video():
    """Testa criação de vídeo"""
    print("\n🎬 Testando criação de vídeo...")
    
    python_cmd = get_python_cmd()
    text = "Este é um teste do sistema de automação de vídeos local. O sistema está funcionando perfeitamente!"
    video_id = "teste_local_001"
    
    print(f"📝 Texto: {text}")
    print(f"🆔 ID: {video_id}")
    print()
    
    # Executa create_video.py
    import subprocess
    try:
        result = subprocess.run([
            python_cmd, "create_video.py", text, video_id
        ], check=True, capture_output=False)
        
        print("\n✅ Teste concluído!")
        
        # Verifica se vídeo foi criado
        video_file = f"videos/video_{video_id}.mp4"
        if os.path.exists(video_file):
            size = os.path.getsize(video_file)
            print(f"🎉 Vídeo criado: {video_file} ({size:,} bytes)")
            return True
        else:
            print(f"❌ Vídeo não foi criado: {video_file}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro durante criação do vídeo: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 50)
    print("🎬 VIDEO AUTOMATION - TESTE DIRETO")
    print("=" * 50)
    print()
    
    # Verifica setup
    if not check_setup():
        return False
    
    # Testa criação de vídeo
    if not test_create_video():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 50)
    print()
    print("📋 PRÓXIMOS PASSOS:")
    print("1. Verifique o vídeo criado na pasta videos/")
    print("2. Para testar servidor Flask:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\python.exe server.py")
    else:
        print("   venv/bin/python server.py")
    print("3. Em outro terminal, teste a API:")
    print("   curl http://localhost:5005/health")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Teste falhou!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Teste cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
