#!/usr/bin/env python3
"""
YouTube Downloader using YouTube Data API v3
مناسب برای دریافت متادیتا، جستجو و مدیریت کانال (نه دانلود مستقیم)
توجه: این متد ویدیو را دانلود نمی‌کند، فقط اطلاعات آن را دریافت می‌کند
"""

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os

class YouTubeAPIClient:
    """کلاینت رسمی YouTube API برای دریافت اطلاعات ویدیو"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
    
    def get_video_info(self, video_id):
        """دریافت اطلاعات کامل یک ویدیو با ID آن"""
        try:
            request = self.youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=video_id
            )
            response = request.execute()
            
            if not response['items']:
                print(f"❌ ویدیو با ID {video_id} پیدا نشد!")
                return None
            
            video = response['items'][0]
            info = {
                'title': video['snippet']['title'],
                'description': video['snippet']['description'],
                'channel': video['snippet']['channelTitle'],
                'views': int(video['statistics'].get('viewCount', 0)),
                'likes': int(video['statistics'].get('likeCount', 0)),
                'comments': int(video['statistics'].get('commentCount', 0)),
                'duration': video['contentDetails']['duration'],
                'published_at': video['snippet']['publishedAt']
            }
            
            return info
            
        except HttpError as e:
            print(f"❌ خطای HTTP: {e}")
            return None
    
    def search_videos(self, query, max_results=10):
        """جستجوی ویدیو در یوتیوب"""
        try:
            request = self.youtube.search().list(
                part="snippet",
                q=query,
                maxResults=max_results,
                type="video"
            )
            response = request.execute()
            
            results = []
            for item in response['items']:
                results.append({
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'channel': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt']
                })
            
            return results
            
        except HttpError as e:
            print(f"❌ خطای HTTP: {e}")
            return []
    
    def get_channel_videos(self, channel_id, max_results=20):
        """دریافت لیست ویدیوهای یک کانال"""
        try:
            # ابتدا آپلودهای کانال را پیدا می‌کنیم
            channels = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id
            ).execute()
            
            if not channels['items']:
                print("کانال پیدا نشد!")
                return []
            
            playlist_id = channels['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # حالا ویدیوها را از پلی‌لیست آپلودها می‌گیریم
            videos = []
            next_page_token = None
            
            for _ in range(2):  # حداکثر ۲ صفحه (حدود 100 ویدیو)
                request = self.youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                for item in response['items']:
                    videos.append({
                        'video_id': item['snippet']['resourceId']['videoId'],
                        'title': item['snippet']['title'],
                        'published_at': item['snippet']['publishedAt']
                    })
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token or len(videos) >= max_results:
                    break
            
            return videos[:max_results]
            
        except HttpError as e:
            print(f"❌ خطای HTTP: {e}")
            return []

def main():
    """اجرای مستقیم اسکریپت از ترمینال"""
    print("=" * 50)
    print("🎥 YouTube API Client - دریافت اطلاعات")
    print("=" * 50)
    
    api_key = input("\n🔑 API Key خود را وارد کنید: ").strip()
    if not api_key:
        print("❌ API Key لازم است!")
        print("📍 راهنمایی: console.cloud.google.com برو و یک API Key بساز")
        return
    
    client = YouTubeAPIClient(api_key)
    
    print("\nچه کاری می‌خواهید انجام دهید؟")
    print("1. دریافت اطلاعات یک ویدیو (با ID)")
    print("2. جستجوی ویدیو با کلمه کلیدی")
    print("3. مشاهده ویدیوهای یک کانال")
    
    choice = input("\nانتخاب کنید (1-3): ").strip()
    
    if choice == "1":
        video_id = input("Video ID را وارد کنید: ").strip()
        info = client.get_video_info(video_id)
        if info:
            print("\n📊 اطلاعات ویدیو:")
            for key, value in info.items():
                print(f"  {key}: {value}")
    
    elif choice == "2":
        query = input("کلمه جستجو: ").strip()
        results = client.search_videos(query)
        print(f"\n📋 نتایج جستجو ({len(results)} مورد):")
        for idx, video in enumerate(results, 1):
            print(f"{idx}. {video['title']} - {video['channel']} (ID: {video['video_id']})")
    
    elif choice == "3":
        channel_id = input("Channel ID را وارد کنید: ").strip()
        videos = client.get_channel_videos(channel_id)
        print(f"\n🎬 ویدیوهای کانال ({len(videos)} مورد):")
        for idx, video in enumerate(videos, 1):
            print(f"{idx}. {video['title']} - {video['published_at']} (ID: {video['video_id']})")
    
    else:
        print("❌ گزینه نامعتبر!")

if __name__ == "__main__":
    main()
