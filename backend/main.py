from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Import our custom modules
from database import init_db, cleanup_old_data
from scheduler import background_fetch_and_store
from routers import router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    
    scheduler = BackgroundScheduler()
    # The normal 5-minute data fetch
    scheduler.add_job(background_fetch_and_store, 'interval', minutes=5)
    
    # Cleanup runs once a day
    scheduler.add_job(cleanup_old_data, 'interval', days=1)
    scheduler.start()
    
    # Run both immediately on startup
    background_fetch_and_store() 
    cleanup_old_data()
    
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

frontend_url = os.getenv("FRONTEND_URL", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)