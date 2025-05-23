import sys
from TTS.api import TTS
import torch
from torch.serialization import safe_globals
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig

texto = sys.argv[1]
id_audio = sys.argv[2]

globals_list = [XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs]

with safe_globals(globals_list):
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=False)

    tts.tts_to_file(
        text=texto,
        speaker_wav="/home/n8n/files/voice_sample.wav",
        language="pt",
        file_path=f"/home/n8n/files/audio_{id_audio}.wav"
    )

