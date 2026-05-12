from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

# Import our custom modules
from database import init_db
from scheduler import background_fetch_and_store
from routers import router

import os
from dotenv import load_dotenv

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(background_fetch_and_store, 'interval', minutes=5)
    scheduler.start()
    
    background_fetch_and_store() # Run once immediately
    
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

# Load the variables from the .env file
load_dotenv()

# Get the URL from .env, but default to "*" if it can't find it
frontend_url = os.getenv("FRONTEND_URL", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect all API endpoints to the main app
app.include_router(router)