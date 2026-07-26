from fastapi import FastAPI, HTTPException, Depends
from database import supabase
from models import UserRegister, UserLogin, Token
from auth import hash_password, verify_password, create_token, get_current_user
# import subprocess
# import json
# from pathlib import Path
# from pydantic import BaseModel
# from typing import List
# import shutil
# from mutagen.mp3 import MP3
app = FastAPI(title="Mini SaaS API", version="1.0")
# class VideoRenderRequest(BaseModel):
#     title: str
#     subtitle: str
#     points: List[str]
#     channel_name: str = "AI Business Insights"

# def get_audio_duration_frames(mp3_path: str, fps: int = 30) -> int:
#     audio = MP3(mp3_path)
#     return int(audio.info.length * fps)

# @app.post("/render")
# def trigger_render(req: VideoRenderRequest):
#     """Trigger a Remotion video render."""

#     VIDEO_DIR = Path("../voice-video-pipeline/video")  # adjust path to your setup
#     OUTPUT_FILE = Path("../voice-video-pipeline/output/final_video.mp4")
#     VOICE_FILE = VIDEO_DIR / "public" / "voice.mp3"
#     # duration = 90 + (len(req.points) * 40 + 60) + 60
#     duration = get_audio_duration_frames(str(VOICE_FILE))

#     props = {
#         "title": req.title,
#         "subtitle": req.subtitle,
#         "points": req.points,
#         "channelName": req.channel_name,
#         "audioFile": "voice.mp3"
#     }

#     # cmd = [
#     #     "npx", "remotion", "render",
#     #     "AIVideoTemplate",
#     #     str(OUTPUT_FILE.resolve()),
#     #     "--props", json.dumps(props),
#     #     "--duration-in-frames", str(duration),
#     #     "--fps", "30",
#     #     "--width", "1920",
#     #     "--height", "1080",
#     # ]
#     npx = shutil.which("npx.cmd")
#     cmd = [
#         npx,
#         "remotion",
#         "render",
#         "src/index.ts",
#         "AIVideoTemplate",
#         str(OUTPUT_FILE.resolve()),
#         "--props", json.dumps(props),
#         "--duration-in-frames", str(duration),
#         "--fps", "30",
#         "--width", "1920",
#         "--height", "1080",
#     ]

#     try:
#         result = subprocess.run(
#             cmd,
#             cwd=str(VIDEO_DIR.resolve()),
#             capture_output=True,
#             text=True,
#             timeout=300
#         )
#         if result.returncode == 0:
#             return {
#                 "status": "success",
#                 "message": "Video rendered successfully",
#                 "output": str(OUTPUT_FILE.resolve())
#             }
#         else:
#             return {
#                 "status": "error",
#                 "message": result.stderr[-300:]
#             }
#     except Exception as e:
#         return {"status": "error", "message": str(e)}


@app.get("/")
def root():
    return {"message": "Mini SaaS API is running"}

# REGISTER a new user
@app.post("/register")
def register(user: UserRegister):
    # Check if email already exists
    existing = supabase.table("users").select("*").eq("email", user.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password and save to Supabase
    hashed = hash_password(user.password)
    supabase.table("users").insert({
        "email": user.email,
        "hashed_password": hashed
    }).execute()
    return {"message": "User registered successfully"}

LOGIN and get a JWT token
@app.post("/login", response_model=Token)
def login(user: UserLogin):
    result = supabase.table("users").select("*").eq("email", user.email).execute()
    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    db_user = result.data[0]
    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# PROTECTED route — only works with a valid token
@app.get("/me")
def get_profile(current_user: str = Depends(get_current_user)):
    return {"email": current_user, "message": "You are authenticated!"}