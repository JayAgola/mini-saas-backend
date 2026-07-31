import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

TOKEN_FILE = "youtube_token.json"

def get_youtube_client():
    """Build and return an authenticated YouTube API client."""
    if not Path(TOKEN_FILE).exists():
        raise FileNotFoundError(
            "youtube_token.json not found. Run get_token.py first."
        )

    with open(TOKEN_FILE) as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data["token"],
        refresh_token=token_data["refresh_token"],
        token_uri=token_data["token_uri"],
        client_id=token_data["client_id"],
        client_secret=token_data["client_secret"],
        scopes=token_data["scopes"]
    )

    # Auto-refresh expired token
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save refreshed token
        token_data["token"] = creds.token
        with open(TOKEN_FILE, "w") as f:
            json.dump(token_data, f, indent=2)

    return build("youtube", "v3", credentials=creds)

def upload_video(
    video_path: str,
    title: str,
    description: str,
    tags: list = None,
    privacy: str = "unlisted"  # "unlisted" for testing, "public" for real uploads
) -> dict:
    """
    Upload a video to YouTube.

    privacy options:
    - "private"  → only you can see it
    - "unlisted" → anyone with the link can see it (good for testing)
    - "public"   → visible to everyone
    """
    if not Path(video_path).exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    youtube = get_youtube_client()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or ["AI", "automation", "content"],
            "categoryId": "22"  # 22 = People & Blogs
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False
        }
    }

    # MediaFileUpload handles large files with chunked upload
    media = MediaFileUpload(
        video_path,
        mimetype="video/mp4",
        resumable=True,  # allows resuming if upload is interrupted
        chunksize=1024 * 1024  # 1MB chunks
    )

    print(f"Uploading: {title}")
    print(f"File: {video_path}")
    print(f"Privacy: {privacy}")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f"Upload progress: {progress}%")

    video_id = response["id"]
    video_url = f"https://youtube.com/watch?v={video_id}"

    print(f"✅ Upload complete!")
    print(f"Video ID: {video_id}")
    print(f"URL: {video_url}")

    return {
        "video_id": video_id,
        "url": video_url,
        "title": title,
        "privacy": privacy
    }