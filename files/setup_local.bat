@echo off
echo ========================================
echo VIDEO AUTOMATION - SETUP LOCAL (Windows)
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nao encontrado! Instale Python 3.11 primeiro.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

REM Cria ambiente virtual
echo.
echo 🐍 Criando ambiente virtual...
if exist "venv" (
    echo Removendo ambiente virtual antigo...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ❌ Erro ao criar ambiente virtual
    pause
    exit /b 1
)

echo ✅ Ambiente virtual criado

REM Ativa ambiente virtual
echo.
echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Atualiza pip
echo.
echo 📦 Atualizando pip...
python -m pip install --upgrade pip

REM Instala dependências
echo.
echo 📦 Instalando dependências Python...
echo    - Flask...
pip install flask==3.0.0

echo    - PyTorch...
pip install torch==2.5.0

echo    - TTS (pode demorar)...
pip install TTS==0.22.0

echo    - MoviePy...
pip install moviepy==1.0.3

echo    - Whisper...
pip install whisper-timestamped==1.14.2

REM Verifica instalação
echo.
echo 🔍 Verificando instalação...
python -c "import flask; print('✅ Flask OK')"
python -c "import torch; print('✅ PyTorch OK')"
python -c "from TTS.api import TTS; print('✅ TTS OK')"
python -c "from moviepy.editor import *; print('✅ MoviePy OK')"
python -c "import whisper_timestamped; print('✅ Whisper OK')"

echo.
echo ========================================
echo ✅ INSTALAÇÃO LOCAL CONCLUÍDA!
echo ========================================
echo.
echo Para ativar o ambiente virtual:
echo   venv\Scripts\activate.bat
echo.
echo Para executar o servidor:
echo   python server.py
echo.
echo Para testar:
echo   curl http://localhost:5005/health
echo.
pause
