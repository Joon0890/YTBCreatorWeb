import re
from .custom_datatime import transform_datetime
from .video_time_length import is_short_video
    

def parse_channel_id_by_name(response):
    """채널 이름으로 채널 ID를 가져오는 함수"""
    if response['items']:
        # 검색 결과에서 채널 ID와 이름 추출
        channel_info = response['items'][0]
        channel_id = channel_info['id']['channelId']
        return channel_id
    else:
        return None


def parse_channel_information(response):
    """채널 정보 응답 처리"""
    channel_info = response["items"][0]
    return {
        "title": channel_info["snippet"]["title"],
        "channel_id": channel_info["id"],
        "thumbnail": channel_info["snippet"]["thumbnails"]["high"]["url"],
        "description": channel_info["snippet"]["description"],
        "subscriber_count": int(channel_info["statistics"]["subscriberCount"]),
        "video_count": int(channel_info["statistics"]["videoCount"]),
        "views_count": int(channel_info["statistics"]["viewCount"]),
    }
    

def parse_comments(response):
    """댓글 응답 처리"""
    comments = []
    for item in response.get("items", []):
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "author": snippet["authorDisplayName"],
            "text": re.sub(r'<.*?>', '', snippet["textDisplay"]),
            "like_count": snippet["likeCount"],
            "publish_time": snippet["publishedAt"],
        })
    return comments

    

def parse_video_statistics(response):
    """비디오 통계 응답 처리"""
    channel_id = response["items"][0]['id']
    for item in response["items"]:
        duration = item["contentDetails"]["duration"]
        publish_time = transform_datetime(item['snippet']['publishedAt'])  # 업로드 날짜 추가
        is_short = is_short_video(duration)
        return {
            "channel_id": channel_id,
            "video_id": item["id"],
            "title": item["snippet"]["title"],
            "view_count": int(item["statistics"].get("viewCount", 0)),
            "like_count": int(item["statistics"].get("likeCount", 0)),
            "comment_count": int(item["statistics"].get("commentCount", 0)),
            "publish_time": publish_time,
            "is_shorts": is_short
        }


def parse_video_ids(response):
    video_data = []

    # response 검증
    if response is None:
        print("[ERROR] Response is None.")
        return []

    if 'items' not in response:
        print("[ERROR] 'items' key is missing in the response.")
        return []

    channel_id = response["items"][0]['id']
    for item in response['items']:
        # 유효한 YouTube 비디오인지 확인
        if item.get('id', {}).get('kind') == "youtube#video":
            video_id = item['id'].get('videoId')
            published_time = transform_datetime(item['snippet'].get('publishedAt'))
            video_data.append({
                'channel_id': channel_id,
                "video_id": video_id,
                "publish_time": published_time
            })

    if not video_data:
        print("[WARNING] No valid video IDs found in the response.")
    
    return video_data


def parse_playlists(response):
    playlist_ids = []
    for item in response.get("items", []):
        playlist_ids.append(item["id"])


def parse_playlist_items(response, all_video_ids):
    all_video_ids = []

    for item in response.get("items", []):
        video_id = item["snippet"]["resourceId"]["videoId"]
        published_time = item["snippet"]["publishedAt"]
        all_video_ids.append({
            "video_id": video_id,
            "publish_time": published_time
        })
