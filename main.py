import os

from fastapi import FastAPI
from dotenv import load_dotenv
from routes import api
from lib.db import engine, db
from lib.firebase import init_firebase
from fastapi.middleware.cors import CORSMiddleware

environment = os.getenv("ENVIRONMENT", "development")

if environment == "development":
    load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the domains you want to allow CORS for
    allow_methods=["*"],  # Set this to the HTTP methods you want to allow CORS for
    allow_headers=["*"],  # Set this to the HTTP headers you want to allow CORS for
)
app.include_router(api.api)


@app.on_event("startup")
def startup():
    print("Starting up")
    db.metadata.create_all(bind=engine, checkfirst=True)
    init_firebase()


@app.get("/")
async def root():
    return {"message": "Hello World"}
