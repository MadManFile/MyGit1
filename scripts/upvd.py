import os
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scope های مورد نیاز برای آپلود به یوتیوب
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    """اتصال به حساب یوتیوب با استفاده از credential.json"""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

def download_video(video_url, output_path):
    """دانلود ویدیو از یک لینک اینترنتی"""
    print(f"⬇️ در حال دانلود ویدیو از {video_url}...")
    response = requests.get(video_url, stream=True)
    with open(output_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print("✅ دانلود کامل شد!")

def upload_video(service, video_file, title, description, tags, category_id, privacy_status):
    """آپلود ویدیو به یوتیوب همراه با metadata"""
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = service.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    response = request.execute()
    print(f"🎉 آپلود با موفقیت انجام شد! شناسه ویدیو: {response['id']}")
    return response['id']

if __name__ == "__main__":
    service = get_authenticated_service()
    
    # ---------- تنظیمات خودت رو اینجا وارد کن ----------
    VIDEO_URL = "https://example.com/path_to_your_video.mp4"  # لینک ویدیو
    LOCAL_VIDEO = "temp_video.mp4"
    VIDEO_TITLE = "عنوان جذاب ویدیو"
    VIDEO_DESC = "توضیحات کامل ویدیو اینجا قرار می‌گیرد."
    VIDEO_TAGS = ["آموزش", "گیت‌هاب", "یوتیوب"]
    CATEGORY_ID = "22"  # 22 یعنی "People & Blogs"
    PRIVACY_STATUS = "public"  # public, private, unlisted
    # ------------------------------------------------
    
    # 1. دانلود ویدیو
    download_video(VIDEO_URL, LOCAL_VIDEO)
    
    # 2. (اینجا بعداً کد ساخت thumbnail رو اضافه می‌کنیم)
    
    # 3. آپلود ویدیو
    upload_video(service, LOCAL_VIDEO, VIDEO_TITLE, VIDEO_DESC, VIDEO_TAGS, CATEGORY_ID, PRIVACY_STATUS)
    
    # 4. پاک کردن فایل موقتی
    os.remove(LOCAL_VIDEO)
    print("🧹 فایل موقتی پاک شد.")
