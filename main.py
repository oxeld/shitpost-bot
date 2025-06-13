# main.py - Shitpost Bot Ana Dosya

import asyncio
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
import os
import datetime
import yt_dlp
from openai import OpenAI
from google.colab import drive

# Sabitler
DRIVE_KLASOR = "MizahVideolari"
VIDEO_URLS = [
    "https://www.tiktok.com/@nurertucan/video/7502879572434767122",
    # Buraya başka video URL'leri eklenebilir
]

# OpenAI API Key (Buraya kendi API anahtarını koy)
OPENAI_API_KEY = "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"

def video_indir(url, dosya_adi):
    ydl_opts = {
        'format': 'best',
        'outtmpl': dosya_adi,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def sahnelere_ayir_ve_altyazi_ekle(video_dosya):
    clip = VideoFileClip(video_dosya)
    duration = int(clip.duration)
    segment = 5
    subtitles = []
    openai = OpenAI(api_key=OPENAI_API_KEY)

    for start in range(0, duration, segment):
        end = min(start + segment, duration)
        mesaj = f"{end-start} saniyelik Türk TikTok sahnesi. Kara mizah, shitpost veya standup tarzında tek satırlık altyazı üret."
        cevap = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": mesaj}]
        )
        altyazi = cevap.choices[0].message.content.strip()
        subtitles.append(((start, end), altyazi))
        print(f"🎭 {start}-{end}sn: {altyazi}")

    gen = lambda txt: TextClip(txt, fontsize=36, font='Arial-Bold', color='white', bg_color='black', size=(clip.w, None)).set_duration(segment)
    subclip = CompositeVideoClip([clip])  # Şimdilik altyazı yok
    return subclip

def main():
    # Google Drive'ı bağla (Colab için, sunucu için kaldırılabilir)
    # drive.mount('/content/drive')
    if not os.path.exists(DRIVE_KLASOR):
        os.makedirs(DRIVE_KLASOR)

    for i, url in enumerate(VIDEO_URLS):
        video_dosya = f"video_{i}.mp4"
        print(f"▶ Video indiriliyor: {url}")
        video_indir(url, video_dosya)

        # Sahnelere ayır ve altyazı ekle (şimdilik altyazısız)
        print("▶ Video düzenleniyor...")
        final_clip = sahnelere_ayir_ve_altyazi_ekle(video_dosya)

        tarih = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        cikti_dosya = os.path.join(DRIVE_KLASOR, f"mizah_video_{tarih}_{i}.mp4")
        final_clip.write_videofile(cikti_dosya, fps=24, codec="libx264")
        print(f"✅ Video kaydedildi: {cikti_dosya}")

if __name__ == "__main__":
    main()