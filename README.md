# Customer Qualifying Chatbot

This project introduces a GPT-powered chatbot designed to qualify potential customers efficiently. It integrates seamlessly into your existing tech stack, offering a cost-effective, easy-to-deploy solution that enhances the initial stages of your sales process.

A low cost interface that serves as our number one chatbot prospecting tool. Easily it can gather intel with only model: **_gpt-3.5-turbo-0125_**

# Overview

The chatbot uses a series of questions to evaluate whether a potential customer aligns with the product or service offered. Successful interactions can lead to the chatbot providing detailed product information and facilitating further engagement steps.

OpenAI's assistant API powers the chatbot's conversational capabilities, allowing it to understand and respond to user queries effectively.

Firebase is utilized as the backend database to store and manage potential customer data securely.

## Prerequisites

Before you begin, ensure you have the following:

- A Firebase account
- An OpenAI API key
- Technologies Used
- Python 3: Main programming language.
- Uvicorn: ASGI server for hosting the application.
- FastAPI: Web framework for building APIs.
- OpenAI: SDK for integrating GPT-powered capabilities.
- Pydantic: Data validation and settings management using Python type annotations.
- Python-dotenv: For loading environment variables from a .env file.
- Firebase Admin: To interact with Firebase services.

## Persona Example

Inside the persona folder, you will find a samm-simon.txt file. Feel free to use this persona and adjust it to your needs. Typically the persona is a fictional character that represents the target audience. This persona will help the AI to understand the context of the conversation and provide more accurate responses. A "persona" or "instruction" can be set inside your assistant settings on the OpenAI platform.

## Configuration

First, prepare your Firebase project(Firestore Database) and download the configuration file to your project directory. Rename the file 'firebase.json'.

Next, create an OpenAI account and generate an API key.

Finally, goto https://platform.openai.com/docs/guides/creating-an-assistant and create the assistant. Note the assistant ID and name.(Set the persona/instruction to the one you created in the persona folder)

### Environment Setup

Set up the required environment variables. You can find an example in example.env. Populate this file with your specific values and rename it:

```bash
mv example.env .env
```

**_Environment variables required:_**

```bash
OPENAI_API_KEY=
ASSISTANT_ID=
ASSISTANT_NAME=
FIREBASE_ID=
```

### Dependencies Installation

Install the necessary Python packages:

```bash
pip install -r requirements.txt
```

## Deployment

### Local Deployment

To run the application locally:

```bash
python3 app.py
```

### Docker Deployment

If you prefer using Docker, execute the provided build script to set up the environment:

```bash
./build.sh
```

This script handles the Docker image creation and container management, making it easy to deploy and update the application.

### Running the Application

For local testing and development, you can start the server using:

```bash
uvicorn app:app --reload
```

This command runs the application with live reloading enabled, which is useful during the development phase.
