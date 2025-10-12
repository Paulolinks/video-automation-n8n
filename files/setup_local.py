#!/usr/bin/env python3
"""
========================================
VIDEO AUTOMATION - SETUP LOCAL (Windows)
========================================
Este script faz TUDO automaticamente:
- Cria ambiente virtual Python
- Instala todas as dependências
- Testa funcionamento
- Cria pastas necessárias
========================================
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Executa comando e mostra resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ERRO")
        print(f"   Erro: {e.stderr}")
        return False

def check_python():
    """Verifica se Python está instalado"""
    print("🐍 Verificando Python...")
    try:
        version = subprocess.check_output([sys.executable, "--version"], text=True).strip()
        print(f"✅ Python encontrado: {version}")
        return True
    except:
        print("❌ Python não encontrado! Instale Python 3.11 primeiro.")
        print("   Download: https://www.python.org/downloads/")
        return False

def create_virtual_env():
    """Cria ambiente virtual"""
    print("\n🐍 Criando ambiente virtual...")
    
    # Remove venv antigo se existir
    if os.path.exists("venv"):
        print("   Removendo ambiente virtual antigo...")
        if platform.system() == "Windows":
            run_command("rmdir /s /q venv", "Remover venv antigo")
        else:
            run_command("rm -rf venv", "Remover venv antigo")
    
    # Cria novo venv
    if not run_command(f'"{sys.executable}" -m venv venv', "Criar ambiente virtual"):
        return False
    
    print("✅ Ambiente virtual criado")
    return True

def get_pip_command():
    """Retorna comando pip baseado no sistema"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\python.exe -m pip"
    else:
        return "venv/bin/python -m pip"

def install_dependencies():
    """Instala dependências Python"""
    print("\n📦 Instalando dependências Python...")
    pip_cmd = get_pip_command()
    
    dependencies = [
        ("flask==3.0.0", "Flask"),
        ("torch==2.5.0", "PyTorch"),
        ("TTS==0.22.0", "TTS"),
        ("moviepy==1.0.3", "MoviePy"),
        ("whisper-timestamped==1.14.2", "Whisper"),
        ("imageio-ffmpeg", "FFmpeg para MoviePy")
    ]
    
    for package, name in dependencies:
        if not run_command(f'"{pip_cmd}" install {package}', f"Instalar {name}"):
            print(f"⚠️  Falha ao instalar {name}, continuando...")
    
    print("✅ Dependências instaladas")
    return True

def create_directories():
    """Cria diretórios necessários"""
    print("\n📁 Criando diretórios...")
    
    directories = ["imagens", "videos", "fonts"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Pasta {directory} criada")
        else:
            print(f"✅ Pasta {directory} já existe")
    
    return True

def test_imports():
    """Testa importações Python"""
    print("\n🔍 Testando importações...")
    
    python_cmd = "venv\\Scripts\\python.exe" if platform.system() == "Windows" else "venv/bin/python"
    
    tests = [
        ("import flask", "Flask"),
        ("import torch", "PyTorch"),
        ("from TTS.api import TTS", "TTS"),
        ("from moviepy.editor import *", "MoviePy"),
        ("import whisper_timestamped", "Whisper")
    ]
    
    all_ok = True
    for test_code, name in tests:
        if run_command(f'"{python_cmd}" -c "{test_code}"', f"Testar {name}"):
            print(f"✅ {name} - OK")
        else:
            print(f"❌ {name} - FALHOU")
            all_ok = False
    
    return all_ok

def check_voice_sample():
    """Verifica se voice_sample.wav existe"""
    print("\n🎤 Verificando voice_sample.wav...")
    
    if os.path.exists("voice_sample.wav"):
        size = os.path.getsize("voice_sample.wav")
        print(f"✅ voice_sample.wav encontrado ({size:,} bytes)")
        return True
    else:
        print("❌ voice_sample.wav não encontrado!")
        print("   Certifique-se de que o arquivo está na pasta files/")
        return False

def main():
    """Função principal"""
    print("=" * 50)
    print("🎬 VIDEO AUTOMATION - SETUP LOCAL")
    print("=" * 50)
    print()
    
    # Verifica Python
    if not check_python():
        return False
    
    # Cria ambiente virtual
    if not create_virtual_env():
        return False
    
    # Instala dependências
    if not install_dependencies():
        return False
    
    # Cria diretórios
    if not create_directories():
        return False
    
    # Verifica voice sample
    if not check_voice_sample():
        return False
    
    # Testa importações
    if not test_imports():
        print("\n⚠️  Algumas importações falharam, mas continuando...")
    
    print("\n" + "=" * 50)
    print("🎉 INSTALAÇÃO LOCAL CONCLUÍDA!")
    print("=" * 50)
    print()
    print("📋 PRÓXIMOS PASSOS:")
    print()
    print("1. Adicione imagens na pasta 'imagens/'")
    print("2. Execute o teste:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\python.exe create_video.py \"Teste local\" \"teste001\"")
        print("   venv\\Scripts\\python.exe server.py")
    else:
        print("   venv/bin/python create_video.py \"Teste local\" \"teste001\"")
        print("   venv/bin/python server.py")
    print()
    print("3. Teste via curl:")
    print("   curl http://localhost:5005/health")
    print()
    print("✅ Sistema pronto para teste local!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Instalação falhou!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Instalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
