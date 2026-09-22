import os
import random
import requests
import google.generativeai as genai
from moviepy.editor import TextClip, ColorClip, CompositeVideoClip, AudioFileClip
from gtts import gTTS

# Setup Gemini API (Old Stable SDK)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Generate Dark Psychology Quote
prompt = "Write a powerful 1-sentence dark psychology or stoic quote for a short video. Do not use quotes."
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(prompt)
quote_text = response.text.strip()
print(f"Generated Quote: {quote_text}")
