import os
import yt_dlp

# כתובת ה-YouTube להורדה
URL = "https://www.youtube.com/watch?v=M4WoInayaqU"

# שמירת קובץ ה-Cookies מתוך משתני ה-GitHub Secrets
COOKIES_CONTENT = os.getenv("YOUTUBE_COOKIES")
COOKIES_FILE = "cookies.txt"

if COOKIES_CONTENT:
    with open(COOKIES_FILE, "w") as f:
        f.write(COOKIES_CONTENT)

# תיקייה מקומית להורדה
OUTPUT_FOLDER = "downloads"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# הגדרת אפשרויות הורדה עם Cookies
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': f"{OUTPUT_FOLDER}/%(title)s.%(ext)s",
    'noplaylist': True,
    'cookiefile': COOKIES_FILE,  # שימוש ב-Cookies להתחברות
}

# הורדת הווידאו
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([URL])

print("✅ הורדה הושלמה בהצלחה!")
