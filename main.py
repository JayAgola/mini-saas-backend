from fastapi import FastAPI, HTTPException, Depends
from database import supabase
from models import UserRegister, UserLogin, Token
from auth import hash_password, verify_password, create_token, get_current_user

app = FastAPI(title="Mini SaaS API", version="1.0")

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

# LOGIN and get a JWT token
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