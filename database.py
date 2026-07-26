import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("SUPABASE_URL")
# URL=URL.strip('"').strip("'")
KEY = os.getenv("SUPABASE_KEY")
# KEY = KEY.strip('"').strip("'")
# print(URL)
# print(KEY)

supabase = create_client(
    URL,
    KEY
)