from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# Rate limiting (requires pip install slowapi)
# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address
# from slowapi.errors import RateLimitExceeded
# limiter = Limiter(key_func=get_remote_address, default_limits=["100 per minute"])
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# limiter_dependency = LimiterDependency(limiter)

from app.database import engine, get_db, Base
from app.routers import users_router as users, records_router as records

app = FastAPI(title="Zorvyn Finance Backend API", version="1.0.0", docs_url="/docs", redoc_url="/redoc")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting (disabled - pip install slowapi to enable)
# limiter = Limiter(key_func=get_remote_address, default_limits=["100 per minute"])
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# limiter_dependency = LimiterDependency(limiter)

app.include_router(users, prefix="/api/v1/users", tags=["users"])
app.include_router(records, prefix="/api/v1/records", tags=["records"])

app.mount("/app/static", StaticFiles(directory="app/static"), name="app_static")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return {"message": "🚀 Zorvyn Finance Backend", "docs": "/docs", "dashboard": "/app/static/index.html"}

Base.metadata.create_all(bind=engine)

