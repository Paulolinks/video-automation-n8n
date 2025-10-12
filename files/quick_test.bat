@echo off
echo ========================================
echo VIDEO AUTOMATION - TESTE RÁPIDO
echo ========================================
echo.

REM Ativa ambiente virtual
call venv\Scripts\activate.bat

echo 🧪 Testando criação de vídeo...
echo.

REM Testa manualmente o create_video.py
echo Executando: python create_video.py "Teste local do sistema" "teste_local_001"
python create_video.py "Teste local do sistema de automação de vídeos" "teste_local_001"

echo.
echo ========================================
echo Teste concluído!
echo.
echo Verifique se o arquivo foi criado em:
echo   videos\video_teste_local_001.mp4
echo.
pause
