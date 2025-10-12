@echo off
echo ========================================
echo VIDEO AUTOMATION - TESTE LOCAL
echo ========================================
echo.

REM Ativa ambiente virtual
echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Verifica se os arquivos necessários existem
echo.
echo 🔍 Verificando arquivos necessários...
if not exist "voice_sample.wav" (
    echo ❌ voice_sample.wav não encontrado!
    echo Certifique-se de que o arquivo está na pasta files/
    pause
    exit /b 1
)
echo ✅ voice_sample.wav encontrado

if not exist "imagens" (
    echo 📁 Criando pasta imagens...
    mkdir imagens
)
echo ✅ Pasta imagens OK

if not exist "videos" (
    echo 📁 Criando pasta videos...
    mkdir videos
)
echo ✅ Pasta videos OK

if not exist "fonts" (
    echo 📁 Criando pasta fonts...
    mkdir fonts
)
echo ✅ Pasta fonts OK

REM Testa importações
echo.
echo 🧪 Testando importações Python...
python -c "
try:
    from TTS.api import TTS
    print('✅ TTS import OK')
except Exception as e:
    print(f'❌ TTS import error: {e}')

try:
    from moviepy.editor import *
    print('✅ MoviePy import OK')
except Exception as e:
    print(f'❌ MoviePy import error: {e}')

try:
    import whisper_timestamped
    print('✅ Whisper import OK')
except Exception as e:
    print(f'❌ Whisper import error: {e}')
"

echo.
echo 🚀 Iniciando servidor local...
echo.
echo Para parar o servidor: Ctrl+C
echo Para testar em outro terminal:
echo   curl http://localhost:5005/health
echo.
echo ========================================

REM Inicia o servidor
python server.py
