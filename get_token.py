from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Scopes needed for YouTube upload
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]

flow = InstalledAppFlow.from_client_secrets_file(
    "client_secrets.json",
    scopes=SCOPES
)

# This opens a browser window for you to sign in
credentials = flow.run_local_server(port=8080)

# Save the token for future use
token_data = {
    "token": credentials.token,
    "refresh_token": credentials.refresh_token,
    "token_uri": credentials.token_uri,
    "client_id": credentials.client_id,
    "client_secret": credentials.client_secret,
    "scopes": list(credentials.scopes)
}

with open("youtube_token.json", "w") as f:
    json.dump(token_data, f, indent=2)

print("✅ Token saved to youtube_token.json")
print(f"Refresh token: {credentials.refresh_token[:20]}...")