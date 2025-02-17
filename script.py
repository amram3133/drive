import os
import yt_dlp
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# קישור הסרטון להורדה (ניתן להחליף ברשימת פלייליסט)
URL = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

# תיקייה מקומית להורדה
OUTPUT_FOLDER = "downloads"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# הגדרת אפשרויות הורדה
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': f"{OUTPUT_FOLDER}/%(title)s.%(ext)s",
    'noplaylist': True,
}

# הורדת הווידאו
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([URL])

# התחברות ל-Google Drive API
CREDENTIALS_JSON = os.getenv("GDRIVE_CREDENTIALS")

if CREDENTIALS_JSON:
    creds = Credentials.from_service_account_info(json.loads(CREDENTIALS_JSON))
    drive_service = build("drive", "v3", credentials=creds)

    # מזהה תיקיית היעד ב-Google Drive
    FOLDER_ID = "YOUR_GOOGLE_DRIVE_FOLDER_ID"

    # העלאת כל הקבצים שהורדו
    for file_name in os.listdir(OUTPUT_FOLDER):
        file_path = os.path.join(OUTPUT_FOLDER, file_name)
        file_metadata = {"name": file_name, "parents": [FOLDER_ID]}
        media = MediaFileUpload(file_path, mimetype="video/mp4")

        uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        print(f"✅ הועלה בהצלחה ל-Google Drive: {file_name}")

else:
    print("❌ לא נמצאו הרשאות Google Drive. בדוק את ה-GitHub Secrets.")
