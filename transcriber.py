import subprocess
import os
from docx import Document
import whisper

url = input("Enter the YouTube video link: ").strip()
wav_file = "temp_audio.wav"

if os.path.exists(wav_file):
    os.remove(wav_file)

print("Downloading and converting audio...")
result = subprocess.run([
    "yt-dlp",
    "--no-playlist",
    "-f", "bestaudio",
    "--extract-audio",
    "--audio-format", "wav",
    "--output", wav_file,
    url
])

if result.returncode != 0 or not os.path.exists(wav_file):
    print("Failed to download or convert the audio.")
    exit(1)

print("Transcribing...")
model = whisper.load_model("base")
result = model.transcribe(wav_file)
text = result["text"].strip()

if text:
    doc = Document()
    doc.add_paragraph(text)
    doc.save("transcription.docx")
    print("Transcription saved as transcription.docx")
else:
    print("⚠No text detected.")

os.remove(wav_file)
print("🧹 Deleted temp_audio.wav")
print("Converted into text and saved as transcription.docx")
    



