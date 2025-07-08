from googleapiclient.discovery import build
from .handling_response import (
    parse_channel_id_by_name, 
    parse_video_statistics, 
    parse_video_ids, 
    parse_channel_information, 
    parse_comments,
    parse_playlists,
    parse_playlist_items
)

class YoutubeApiManager:
    def __init__(self, api_key, channel_id=None, channel_name=None):
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self.channel_name = channel_name
        self.channel_id = channel_id or self.get_channel_id_by_name()

    def get_channel_id_by_name(self):
        response = self.youtube.search().list(
            part='snippet',
            q=self.channel_name,
            type='channel', 
            maxResults=1
            ).execute()
        return parse_channel_id_by_name(response) 

    def get_channel_information(self):
        response = self.youtube.channels().list(
            part="snippet,statistics",
            id=self.channel_id
            ).execute()
        return parse_channel_information(response) 

    def get_video_statistics(self, video_id):
        response = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
            ).execute()
        return parse_video_statistics(response) 

    def get_comments(self, video_id):
        try:
            response = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                order="relevance"
                ).execute()
            return parse_comments(response) 
        except Exception as e:
            print(f"[ERROR] Failed to fetch comments for video_id={video_id}: {e}")
            return None
        
    
    def get_video_ids(self):
        response = self.youtube.search().list(
            part="snippet",
            channelId=self.channel_id,
            maxResults=10,
            order="date",
            ).execute()
        
        return parse_video_ids(response) 
    
    def get_all_video_ids(self):
        next_page_token = None
        video_data = []

        while True:
            response = self.youtube.search().list(
                part="snippet",
                channelId=self.channel_id,
                maxResults=50,
                pageToken=next_page_token,
                type="video",
                order="date"  
                ).execute()
            
            parsed = parse_video_ids(response) 
            video_data.extend(parsed)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break        
                
        return video_data


    def get_all_playlists(self):
        playlist_ids = []
        next_page_token = None

        while True:
            response = self.youtube.playlists().list(
                part="snippet",
                channelId=self.channel_id,
                maxResults=50,
                pageToken=next_page_token
                ).execute()

            parsed = parse_playlists(response)
            playlist_ids.extend(parsed)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
        
        return playlist_ids        

    def get_all_playlist_items(self, playlist_ids):
        all_video_ids = []

        for playlist_id in playlist_ids:
            next_page_token = None

            while True:
                # playlistItems.list API 호출
                response = self.youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                    ).execute()
                
                parsed = parse_playlist_items(response)
                all_video_ids.extend(parsed)

                # 다음 페이지로 이동
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break
        
        return all_video_ids