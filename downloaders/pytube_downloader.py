#!/usr/bin/env python3
"""
YouTube Downloader using Pytube
کتابخانه ساده و سبک برای دانلود سریع ویدیوها
"""

from pytube import YouTube
from pytube.exceptions import PytubeError
import os
import sys

def download_with_pytube(url, output_path="downloads", quality="highest"):
    """
    دانلود ویدیو با pytube
    
    Args:
        url: لینک ویدیو یوتیوب
        output_path: مسیر ذخیره فایل
        quality: کیفیت (highest, lowest, audio)
    """
    
    os.makedirs(output_path, exist_ok=True)
    
    try:
        print(f"\n🎬 شروع دانلود با Pytube...")
        print(f"📎 لینک: {url}")
        print(f"📁 مسیر: {output_path}")
        print("-" * 50)
        
        # ایجاد شیء YouTube
        yt = YouTube(url)
        
        # نمایش اطلاعات ویدیو
        print(f"📺 عنوان: {yt.title}")
        print(f"⏱️  مدت زمان: {yt.length} ثانیه")
        print(f"👁️ بازدیدها: {yt.views:,}")
        print(f"👍 لایک: {yt.rating}")
        
        # انتخاب استریم مناسب
        if quality == "highest":
            stream = yt.streams.get_highest_resolution()
        elif quality == "lowest":
            stream = yt.streams.get_lowest_resolution()
        elif quality == "audio":
            stream = yt.streams.get_audio_only()
        else:
            stream = yt.streams.get_highest_resolution()
        
        # دانلود فایل
        print(f"\n⬇️ در حال دانلود...")
        downloaded_file = stream.download(output_path=output_path)
        
        # تغییر نام فایل صوتی به mp3
        if quality == "audio" and downloaded_file.endswith('.mp4'):
            new_name = downloaded_file.replace('.mp4', '.mp3')
            os.rename(downloaded_file, new_name)
            downloaded_file = new_name
        
        file_size = os.path.getsize(downloaded_file) / (1024 * 1024)
        print(f"\n✅ دانلود کامل شد!")
        print(f"💾 مسیر فایل: {downloaded_file}")
        print(f"📦 حجم: {file_size:.2f} MB")
        
        return True
        
    except PytubeError as e:
        print(f"❌ خطای Pytube: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ خطای ناشناخته: {str(e)}")
        return False

def main():
    """اجرای مستقیم اسکریپت از ترمینال"""
    print("=" * 50)
    print("🎥 YouTube Downloader - نسخه Pytube")
    print("=" * 50)
    
    url = input("\n🔗 لینک یوتیوب را وارد کنید: ").strip()
    if not url:
        print("❌ لینک معتبر وارد کنید!")
        return
    
    print("\nکیفیت مورد نظر:")
    print("1. بهترین کیفیت")
    print("2. پایین‌ترین کیفیت")
    print("3. فقط صوت (MP3)")
    
    choice = input("\nانتخاب کنید (1-3): ").strip()
    
    quality_map = {
        "1": "highest",
        "2": "lowest",
        "3": "audio"
    }
    
    quality = quality_map.get(choice, "highest")
    download_with_pytube(url, "downloads_pytube", quality)

if __name__ == "__main__":
    main()
