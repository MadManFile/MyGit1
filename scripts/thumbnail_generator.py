import subprocess
import os

def generate_thumbnail(video_path, output_path, title_text):
    """ساخت thumbnail حرفه‌ای با استفاده از ffmpeg"""
    if not os.path.exists(video_path):
        print(f"❌ خطا: ویدیو در مسیر {video_path} پیدا نشد!")
        return None
        
    print(f"🎨 در حال ساخت thumbnail برای ویدیو...")
    
    # دستور جادویی ffmpeg برای گرفتن یک فریم از میانه ویدیو و اضافه کردن متن روی آن
    # این دستور همزمان ۴ کار رو انجام میده:
    # 1. از 40% ویدیو یک فریم برمیداره
    # 2. ابعادش رو به 1280*720 تغییر میده
    # 3. یک متن (عنوان ویدیو) رو با سایه و کادر روی اون مینویسه
    # 4. فایل نهایی رو با کیفیت خوب save میکنه
    command = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-ss", "40%", "-i", video_path,
        "-frames:v", "1",
        "-vf", f"scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
                f"drawtext=text='{title_text}':fontcolor=white:fontsize=68:"
                f"x=(w-text_w)/2:y=(h-text_h)/2:shadowcolor=black@0.8:shadowx=5:shadowy=5:"
                f"box=1:boxcolor=black@0.5:boxborderw=20",
        "-q:v", "3", output_path
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        print(f"✅ Thumbnail با موفقیت ساخته شد: {output_path}")
        return output_path
    else:
        print(f"❌ خطا در ساخت thumbnail: {result.stderr}")
        return None

# مثال استفاده:
# generate_thumbnail("temp_video.mp4", "thumbnail.jpg", "عنوان ویدیو")
