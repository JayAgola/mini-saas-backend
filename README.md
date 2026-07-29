"# mini-saas-backend" 
# Mini SaaS Backend API

🚀 **Live Demo:** https://your-railway-url.up.railway.app/docs

## Endpoints
| Method | Route | Description | Auth required |
|--------|-------|-------------|---------------|
| GET | / | Health check | No |
| POST | /register | Register new user | No |
| POST | /login | Login, get JWT token | No |
| GET | /me | Get current user profile | Yes |

## Tech Stack
- FastAPI — Python web framework
- Supabase — PostgreSQL database (free tier)
- JWT — authentication
- Railway — hosting (free tier)

## Run locally
1. Clone the repo
2. pip install -r requirements.txt
3. Add .env with your Supabase + secret keys
4. uvicorn main:app --reload


## Run with Docker

# Pull from Docker Hub
docker pull yourusername/mini-saas-api:v1

# Run (add your own environment variables)
docker run -p 8000:8000 --env-file .env.docker yourusername/mini-saas-api:v1

# Or build locally
docker build -t mini-saas-api .
docker run -p 8000:8000 --env-file .env.docker mini-saas-api