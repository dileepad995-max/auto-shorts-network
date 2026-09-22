import os
import asyncio
import json
import requests
import edge_tts
from google import genai
from moviepy.editor import VideoFileClip, AudioFileClip

# 1. Setup API Keys
gemini_key = os.environ.get("GEMINI_API_KEY")
pexels_key = os.environ.get("PEXELS_API_KEY")

client = genai.Client(api_key=gemini_key)

# 2. Generate Dark Psychology / Stoic Script via Gemini API
prompt = """
Generate a powerful 30-second viral Dark Psychology or Stoic Mindset short script.
It must be intriguing, psychological, and captivating for a global audience.
Return ONLY a raw JSON object with this exact structure:
{
  "script": "The spoken voiceover text (around 40-50 words max).",
  "search_query": "1 or 2 keywords for background video on Pexels (e.g. 'dark moody man', 'stoic statue', 'rainy city')"
}
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
)

text_resp = response.text.strip()
if text_resp.startswith("```json"):
    text_resp = text_resp[7:-3].strip()
elif text_resp.startswith("```"):
    text_resp = text_resp[3:-3].strip()

data = json.loads(text_resp)
script_text = data["script"]
search_query = data["search_query"]

print(f"Generated Script: {script_text}")
print(f"Video Search Query: {search_query}")

# 3. Generate Voiceover using Edge TTS
async def generate_audio():
    communicate = edge_tts.Communicate(script_text, "en-US-ChristopherNeural")
    await communicate.save("voiceover.mp3")

asyncio.run(generate_audio())

# 4. Fetch Background Video from Pexels
headers = {"Authorization": pexels_key}
pexels_url = f"https://api.pexels.com/videos/search?query={search_query}&per_page=5&orientation=portrait"
res = requests.get(pexels_url, headers=headers).json()

video_download_url = None
if res.get("videos"):
    for video in res["videos"]:
        for vf in video["video_files"]:
            if vf.get("width") and vf.get("height") and vf["height"] > vf["width"]:
                video_download_url = vf["link"]
                break
        if video_download_url:
            break

if not video_download_url and res.get("videos"):
    video_download_url = res["videos"][0]["video_files"][0]["link"]

# Fallback video if search yields nothing
if not video_download_url:
    fallback_url = "https://api.pexels.com/videos/search?query=dark+moody&per_page=1&orientation=portrait"
    res = requests.get(fallback_url, headers=headers).json()
    video_download_url = res["videos"][0]["video_files"][0]["link"]

video_data = requests.get(video_download_url).content
with open("background.mp4", "wb") as f:
    f.write(video_data)

# 5. Assemble Final Video with MoviePy
audio_clip = AudioFileClip("voiceover.mp3")
video_clip = VideoFileClip("background.mp4")

# Adjust Video Duration to match Audio
if video_clip.duration < audio_clip.duration:
    video_clip = video_clip.loop(duration=audio_clip.duration)
else:
    video_clip = video_clip.subclip(0, audio_clip.duration)

final_clip = video_clip.set_audio(audio_clip)
final_clip.write_videofile("output.mp4", fps=24, codec="libx264", audio_codec="aac")

print("Automation Completed! Video saved as output.mp4")
