import sys
import os
import subprocess
import whisper

video_id = sys.argv[1]
audio_path = f"/home/n8n/files/audio_{video_id}.wav"
video_path = f"/home/n8n/files/video_{video_id}.mp4"
srt_path = f"/home/n8n/files/audio_{video_id}.srt"
output_path = f"/home/n8n/files/video_{video_id}_final.mp4"

# 1. Transcreve o áudio com Whisper
model = whisper.load_model("base")
result = model.transcribe(audio_path)

# 2. Salva como .srt
with open(srt_path, "w", encoding="utf-8") as f:
    for i, segment in enumerate(result["segments"]):
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]

        def format_time(seconds):
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            s = int(seconds % 60)
            ms = int((seconds % 1) * 1000)
            return f"{h:02}:{m:02}:{s:02},{ms:03}"

        f.write(f"{i+1}\n")
        f.write(f"{format_time(start)} --> {format_time(end)}\n")
        f.write(f"{text.strip()}\n\n")

# 3. Adiciona a legenda no centro do vídeo com FFmpeg
ffmpeg_cmd = [
    "ffmpeg",
    "-i", video_path,
    "-vf", f"subtitles={srt_path}:force_style='Alignment=2,FontName=Active Heart,FontSize=36,PrimaryColour=&H00FFFF00'",
    "-c:a", "copy",
    output_path
]

subprocess.run(ffmpeg_cmd, check=True)
print(f"✅ Vídeo final criado com legenda em {output_path}")
