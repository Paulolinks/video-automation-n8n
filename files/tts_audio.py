from TTS.api import TTS

# Texto a ser falado
texto = "Acredite no seu processo. Cada passo que você dá hoje aproxima você do seu próximo nível. Continue avançando."

# Instanciar modelo
tts = TTS(model_name="tts_models/pt/cv/vits", progress_bar=False, gpu=False)

# Gerar e salvar áudio
tts.tts_to_file(text=texto, file_path="/home/n8n/files/audio.wav")

