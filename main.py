import os
import random
import requests
from google import genai
from moviepy.editor import TextClip, ColorClip, CompositeVideoClip, AudioFileClip
from gtts import gTTS

# Setup Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Generate Dark Psychology Quote
prompt = "Write a powerful 1-sentence dark psychology or stoic quote for a short video. Do not use quotes."
response = client.models.generate_content(
    model=gemini-1.5-flash,
    contents=prompt,
)
quote_text = response.text.strip()
print(f"Generated Quote: {quote_text}")

# Generate Audio using gTTS
tts = gTTS(text=quote_text, lang='en', slow=False)
tts.save("audio.mp3")

# Video Specs (Vertical 1080x1920)
audio_clip = AudioFileClip("audio.mp3")
duration = audio_clip.duration

# Background Clip (Dark Theme)
bg_clip = ColorClip(size=(1080, 1920), color=(15, 15, 20)).set_duration(duration)

# Text Clip
txt_clip = TextClip(
    quote_text,
    fontsize=50,
    color='white',
    font='DejaVu-Sans-Bold',
    method='caption',
    size=(900, None)
).set_position('center').set_duration(duration)

# Combine Video and Audio
final_video = CompositeVideoClip([bg_clip, txt_clip]).set_audio(audio_clip)
final_video.write_videofile("output.mp4", fps=24, codec='libx264', audio_codec='aac')

print("Video generation complete: output.mp4")
