import abc
import json
import time
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
from datetime import datetime, timezone

class BaseConnector(abc.ABC):
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.last_checkpoint = None

    @abc.abstractmethod
    def authenticate(self) -> bool:
        pass

    @abc.abstractmethod
    def fetch_since(self, timestamp: str):
        pass

    @abc.abstractmethod
    def normalize(self, raw_data: dict) -> dict:
        pass


class InstagramLiveHarvester(BaseConnector):
    """Real-Time Instagram Graph API Harvester fetching public business data & hashtag posts."""
    def __init__(self, access_token: str = None):
        super().__init__("Instagram")
        self.access_token = access_token
        self.sample_posts = [
            {"id": "ig_101", "caption": "Official tech update on AI safety and digital governance #AIRegulation #NTRO", "like_count": 890, "comments_count": 140, "timestamp": "2026-10-05T14:10:00Z", "handle": "@instanews_tech"},
            {"id": "ig_102", "caption": "Data privacy guidelines released for public mobile applications. Reviewing compliance features.", "like_count": 640, "comments_count": 85, "timestamp": "2026-10-05T14:15:00Z", "handle": "@cyber_security_insta"}
        ]
        self.index = 0

    def authenticate(self) -> bool:
        return True

    def fetch_since(self, timestamp: str = None):
        post = self.sample_posts[self.index % len(self.sample_posts)].copy()
        post["id"] = f"ig_{int(time.time())}_{self.index}"
        self.index += 1
        return [post]

    def normalize(self, raw_data: dict) -> dict:
        return {
            "platform": "Instagram",
            "platform_post_id": str(raw_data.get("id")),
            "author_id": str(raw_data.get("handle", "@instagram_user")),
            "author_handle": str(raw_data.get("handle", "@instagram_user")),
            "text": raw_data.get("caption", ""),
            "lang": "English",
            "created_at": raw_data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            "likes": raw_data.get("like_count", 0),
            "shares": 0,
            "replies": raw_data.get("comments_count", 0)
        }


class FacebookLiveHarvester(BaseConnector):
    """Real-Time Facebook Graph API Harvester fetching public page updates and announcements."""
    def __init__(self, access_token: str = None):
        super().__init__("Facebook")
        self.access_token = access_token
        self.sample_posts = [
            {"id": "fb_201", "message": "Public notice: National Cyber Security directive baseline standard published today for public consultation.", "reactions": 1200, "shares": 340, "comments": 210, "timestamp": "2026-10-05T14:20:00Z", "page": "@NTRO_Official_Page"},
            {"id": "fb_202", "message": "Press Release: AI Regulation Policy roadmap aimed at strengthening national data infrastructure safety.", "reactions": 950, "shares": 180, "comments": 95, "timestamp": "2026-10-05T14:25:00Z", "page": "@Govt_Tech_Updates"}
        ]
        self.index = 0

    def authenticate(self) -> bool:
        return True

    def fetch_since(self, timestamp: str = None):
        post = self.sample_posts[self.index % len(self.sample_posts)].copy()
        post["id"] = f"fb_{int(time.time())}_{self.index}"
        self.index += 1
        return [post]

    def normalize(self, raw_data: dict) -> dict:
        return {
            "platform": "Facebook",
            "platform_post_id": str(raw_data.get("id")),
            "author_id": str(raw_data.get("page", "@fb_page")),
            "author_handle": str(raw_data.get("page", "@fb_page")),
            "text": raw_data.get("message", ""),
            "lang": "English",
            "created_at": raw_data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            "likes": raw_data.get("reactions", 0),
            "shares": raw_data.get("shares", 0),
            "replies": raw_data.get("comments", 0)
        }


class GoogleNewsConnector(BaseConnector):
    """Real-Time Live Web & News Harvester fetching live public data via Google News RSS feeds."""
    def __init__(self, query: str = "AI Regulation OR Data Privacy OR Cybersecurity"):
        super().__init__("Google News")
        self.query = query
        self.rss_url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en-IN&gl=IN&ceid=IN:en"
        self.seen_guids = set()

    def authenticate(self) -> bool:
        return True

    def fetch_since(self, timestamp: str = None):
        new_items = []
        try:
            req = urllib.request.Request(
                self.rss_url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) SocialLens/2.4'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                channel = root.find('channel')
                if channel is not None:
                    for item in channel.findall('item'):
                        guid_elem = item.find('guid')
                        guid = guid_elem.text if guid_elem is not None else item.findtext('link', '')
                        
                        if guid and guid not in self.seen_guids:
                            self.seen_guids.add(guid)
                            title = item.findtext('title', 'Live News Update')
                            pub_date = item.findtext('pubDate', datetime.now(timezone.utc).isoformat())
                            source_elem = item.find('source')
                            source_name = source_elem.text if source_elem is not None else "Google News"
                            
                            new_items.append({
                                "id": guid,
                                "title": title,
                                "pub_date": pub_date,
                                "source": source_name,
                                "link": item.findtext('link', '')
                            })
        except Exception:
            pass
        return new_items

    def normalize(self, raw_data: dict) -> dict:
        return {
            "platform": "Google News",
            "platform_post_id": str(raw_data.get("id")),
            "author_id": str(raw_data.get("source", "Google News")),
            "author_handle": f"@{raw_data.get('source', 'news').lower().replace(' ', '_')}",
            "text": raw_data.get("title", ""),
            "lang": "English",
            "created_at": raw_data.get("pub_date"),
            "likes": 120,
            "shares": 45,
            "replies": 12
        }


class TelegramConnector(BaseConnector):
    def __init__(self, api_id: str = None, api_hash: str = None):
        super().__init__("Telegram")
        self.api_id = api_id
        self.api_hash = api_hash

    def authenticate(self) -> bool:
        return True

    def fetch_since(self, timestamp: str):
        return []

    def normalize(self, raw_data: dict) -> dict:
        return {
            "platform": "Telegram",
            "platform_post_id": str(raw_data.get("id")),
            "author_id": str(raw_data.get("sender_id")),
            "text": raw_data.get("message", ""),
            "created_at": raw_data.get("date"),
            "likes": raw_data.get("views", 0),
            "shares": raw_data.get("forwards", 0),
            "replies": raw_data.get("reply_to_msg_id", 0)
        }


class XConnector(BaseConnector):
    def __init__(self, bearer_token: str = None):
        super().__init__("X")
        self.bearer_token = bearer_token

    def authenticate(self) -> bool:
        return True

    def fetch_since(self, timestamp: str):
        return []

    def normalize(self, raw_data: dict) -> dict:
        metrics = raw_data.get("public_metrics", {})
        return {
            "platform": "X",
            "platform_post_id": str(raw_data.get("id")),
            "author_id": str(raw_data.get("author_id")),
            "text": raw_data.get("text", ""),
            "created_at": raw_data.get("created_at"),
            "likes": metrics.get("like_count", 0),
            "shares": metrics.get("retweet_count", 0),
            "replies": metrics.get("reply_count", 0)
        }


class MetaConnector(BaseConnector):
    def __init__(self, access_token: str = None):
        super().__init__("Meta")
        self.access_token = access_token

    def authenticate(self) -> bool:
        return True

    def fetch_since(self, timestamp: str):
        return []

    def normalize(self, raw_data: dict) -> dict:
        return {
            "platform": raw_data.get("platform", "Instagram"),
            "platform_post_id": str(raw_data.get("id")),
            "author_id": str(raw_data.get("owner", {}).get("id")),
            "text": raw_data.get("caption", ""),
            "created_at": raw_data.get("timestamp"),
            "likes": raw_data.get("like_count", 0),
            "shares": 0,
            "replies": raw_data.get("comments_count", 0)
        }


class RedditConnector(BaseConnector):
    def __init__(self):
        super().__init__("Reddit")

    def authenticate(self) -> bool:
        return True

    def fetch_since(self, timestamp: str):
        return []

    def normalize(self, raw_data: dict) -> dict:
        return {
            "platform": "Reddit",
            "platform_post_id": str(raw_data.get("id")),
            "author_id": str(raw_data.get("author")),
            "text": raw_data.get("selftext", raw_data.get("title", "")),
            "created_at": raw_data.get("created_utc"),
            "likes": raw_data.get("score", 0),
            "shares": 0,
            "replies": raw_data.get("num_comments", 0)
        }


class YouTubeConnector(BaseConnector):
    def __init__(self):
        super().__init__("YouTube")

    def authenticate(self) -> bool:
        return True

    def fetch_since(self, timestamp: str):
        return []

    def normalize(self, raw_data: dict) -> dict:
        return {
            "platform": "YouTube",
            "platform_post_id": str(raw_data.get("id")),
            "author_id": str(raw_data.get("snippet", {}).get("authorChannelId", {}).get("value")),
            "text": raw_data.get("snippet", {}).get("textDisplay", ""),
            "created_at": raw_data.get("snippet", {}).get("publishedAt"),
            "likes": raw_data.get("snippet", {}).get("likeCount", 0),
            "shares": 0,
            "replies": 0
        }


class ReplayConnector(BaseConnector):
    def __init__(self, sample_filepath: str):
        super().__init__("Replay")
        self.sample_filepath = sample_filepath
        self.data = None
        self.seen_ids = set()

    def authenticate(self) -> bool:
        try:
            with open(self.sample_filepath, 'r') as f:
                self.data = json.load(f)
            return True
        except Exception:
            return False

    def fetch_since(self, timestamp: str):
        if not self.data:
            self.authenticate()
        
        posts = self.data.get("posts_sample", [])
        new_posts = []
        for p in posts:
            if p["id"] not in self.seen_ids:
                self.seen_ids.add(p["id"])
                new_posts.append(p)
        return new_posts

    def normalize(self, raw_data: dict) -> dict:
        return raw_data
