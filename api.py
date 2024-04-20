from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

from app.routes.router import router, configure_router

# Load environment variables from the .env file at the start of the application.
load_dotenv()

# Retrieve necessary configuration variables from the environment.
API_KEY = os.getenv('API_KEY')
ASSISTANT_NAME = os.getenv('ASSISTANT_NAME')
ASSISTANT_ID = os.getenv('ASSISTANT_ID')

# Configure the router with the API key and assistant details.
configure_router(API_KEY, ASSISTANT_NAME, ASSISTANT_ID)

# Create an instance of FastAPI.
app = FastAPI()

# Include the configured router into the main application.
app.include_router(router)

# Mount a directory of static files under the root path.
app.mount("/", StaticFiles(directory="public", html=True), name="public")
