from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

from app.sessions.user_session import RateLimiter
from app.sessions.chat_session import ChatSession
from app.sessions.data_session import DataManager
from app.managers.thread_manager import ThreadManager
from app.managers.assistant_manager import AssistantManager
from openai import AsyncOpenAI

router = APIRouter()

rate_limiter = RateLimiter()

class ChatRequest(BaseModel):
    user_ip: str
    message: str
    threadId: str = None

def configure_router(api_key: str = None, assistant_name: str = None, assistant_id: str = None, firebase_id: str = None):
    """
    Configure the router with specific API key and assistant details.
    Args:
    api_key (str): The API key for OpenAI.
    assistant_name (str): Name of the assistant.
    assistant_id (str): Unique identifier for the assistant.

    This function allows for overriding the default environment variable settings.
    """
    global API_KEY, ASSISTANT_NAME, ASSISTANT_ID, FIREBASE_ID
    API_KEY = api_key 
    ASSISTANT_NAME = assistant_name 
    ASSISTANT_ID = assistant_id 
    FIREBASE_ID = firebase_id 

@router.post("/chat")
async def chat(chat_request: ChatRequest):
    """
    Handle a chat request by processing the user's message and returning a response.
    Args:
    chat_request (ChatRequest): The request payload containing the user IP, message, and optional thread ID.

    Returns:
    dict: A dictionary containing the assistant's response and the thread ID used.
    """
    if not chat_request.user_ip:
        raise HTTPException(status_code=400, detail="User IP address is required.")

    # Check if the user is allowed to make a request
    if not await rate_limiter.is_allowed(chat_request.user_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")

    # Initialize API client and managers using global settings
    openai_async_client = AsyncOpenAI(api_key=API_KEY)
    thread_manager = ThreadManager(openai_async_client)
    assistant_manager = AssistantManager(openai_async_client)
    data_manager = DataManager(API_KEY, FIREBASE_ID)

    # Check if the string size is within the limits of 120 characters
    if len(chat_request.message) > 200:
        return {"assistant_response": "Please keep your message under 200 characters.", "current_rate": rate_limiter.requests[chat_request.user_ip]}

    # Process and store data received in the request
    await data_manager.parse_and_store_data(chat_request.user_ip, chat_request.message)

    # Create or retrieve a chat session
    session = ChatSession(thread_manager, assistant_manager, ASSISTANT_NAME, "gpt-3.5-turbo-0125", ASSISTANT_ID)
    thread_id = chat_request.threadId or await session.get_or_create_thread()

    # Retrieve the latest response from the chat session
    response = await session.get_latest_response(chat_request.message, thread_id)
    if response:
        return {"assistant_response": response, "thread_id": thread_id, "current_rate": rate_limiter.requests[chat_request.user_ip]}
    else:
        raise HTTPException(status_code=503, detail="Our chat system is currently unavailable. Please try again later.")
