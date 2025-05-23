import whisper_timestamped
import sys
import json

audio_path = sys.argv[1]
output_path = sys.argv[2]

model = whisper_timestamped.load_model("base")  # ou "small", "medium" etc.

result = whisper_timestamped.transcribe(model, audio_path)

with open(output_path, "w") as f:
    json.dump(result["segments"], f, indent=2)
