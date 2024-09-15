import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from dotenv import load_dotenv


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

origins = ["*"]

load_dotenv()

from routers.events import router as events_router


# Dictionary to hold MongoDB client (or other resources)
db_client = {}

# Lifespan context manager for managing startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to MongoDB on startup
    app.mongodb_client = AsyncIOMotorClient(os.getenv("DB_URL"))  # Adjust your MongoDB URI as necessary
    app.mongodb = app.mongodb_client["JoinTable"]  # Replace with your actual database name
    print("Connected to MongoDB")
    await app.mongodb.command("ismaster")

    yield
    # Cleanup: Close MongoDB connection on shutdown
    app.mongodb_client.close()
    print("MongoDB connection closed")

app = FastAPI(middleware=middleware, lifespan=lifespan)


app.include_router(events_router, prefix="/event", tags=["events"])




@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


