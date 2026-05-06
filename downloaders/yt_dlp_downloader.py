#!/usr/bin/env python3
"""
YouTube Downloader using yt-dlp
قوی‌ترین ابزار دانلود از یوتیوب - پشتیبانی از پلی‌لیست، زیرنویس، و کیفیت‌های مختلف
"""

import yt_dlp
import os
import sys

def download_with_ytdlp(url, output_path="downloads", quality="best"):
    """
    دانلود ویدیو با yt-dlp
    
    Args:
        url: لینک ویدیو یا پلی‌لیست یوتیوب
        output_path: مسیر ذخیره فایل‌ها
        quality: کیفیت (best, 1080, 720, audio)
    """
    
    # تنظیمات کیفیت
    if quality == "best":
        format_spec = "bestvideo+bestaudio/best"
    elif quality == "1080":
        format_spec = "bestvideo[height<=1080]+bestaudio/best"
    elif quality == "720":
        format_spec = "bestvideo[height<=720]+bestaudio/best"
    elif quality == "audio":
        format_spec = "bestaudio/best"
    else:
        format_spec = "best"
    
    # تنظیمات yt-dlp
    ydl_opts = {
        'format': format_spec,
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': False,
        
        # اگر audio خواستی
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if quality == "audio" else [],
    }
    
    # اطمینان از وجود پوشه خروجی
    os.makedirs(output_path, exist_ok=True)
    
    try:
        print(f"\n🎬 شروع دانلود با yt-dlp...")
        print(f"📎 لینک: {url}")
        print(f"📁 مسیر: {output_path}")
        print(f"🎯 کیفیت: {quality}")
        print("-" * 50)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # نمایش اطلاعات ویدیو
            if 'entries' in info:  # پلی‌لیست
                print(f"\n✅ دانلود پلی‌لیست کامل شد! تعداد ویدیوها: {len(info['entries'])}")
            else:  # تک ویدیو
                print(f"\n✅ دانلود کامل شد!")
                print(f"📺 عنوان: {info.get('title', 'Unknown')}")
                print(f"⏱️  مدت زمان: {info.get('duration', 0)} ثانیه")
                
        return True
        
    except Exception as e:
        print(f"❌ خطا در دانلود: {str(e)}")
        return False

def main():
    """اجرای مستقیم اسکریپت از ترمینال"""
    print("=" * 50)
    print("🎥 YouTube Downloader - نسخه yt-dlp")
    print("=" * 50)
    
    url = input("\n🔗 لینک یوتیوب را وارد کنید: ").strip()
    if not url:
        print("❌ لینک معتبر وارد کنید!")
        return
    
    print("\nکیفیت مورد نظر:")
    print("1. بهترین کیفیت (best)")
    print("2. 1080p")
    print("3. 720p")
    print("4. فقط صوت (MP3)")
    
    choice = input("\nانتخاب کنید (1-4): ").strip()
    
    quality_map = {
        "1": "best",
        "2": "1080",
        "3": "720",
        "4": "audio"
    }
    
    quality = quality_map.get(choice, "best")
    download_with_ytdlp(url, "downloads_ytdlp", quality)

if __name__ == "__main__":
    main()
