# YouTube OAuth Setup Guide

## Why OAuth?
YouTube requires channel owner permission to upload videos.
OAuth lets the channel owner sign in once — your system
uploads automatically from then on.

## One-time setup steps

### 1. Google Cloud Console
1. Go to console.cloud.google.com
2. Select your project
3. APIs & Services → Credentials → Create OAuth Client ID
4. Application type: Desktop app
5. Download JSON → save as client_secrets.json

### 2. Configure OAuth Consent Screen
1. APIs & Services → OAuth consent screen
2. User type: External
3. Add your Google email as a test user
4. Scopes: YouTube Data API v3

### 3. Generate token (run once)
python get_token.py
# Opens browser → sign in → allows access
# Saves youtube_token.json automatically

### 4. Test upload
# Start FastAPI: uvicorn main:app --reload
# POST /upload with video_path, title, description
# First upload goes as "unlisted" for safety

## Token management
- Tokens auto-refresh via the refresh_token
- Refresh tokens don't expire unless revoked
- Store youtube_token.json securely — never commit to GitHub

## Privacy settings
- private: only you
- unlisted: anyone with link (use for testing)
- public: visible to everyone (use for production)