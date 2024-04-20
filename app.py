import uvicorn

if __name__ == "__main__":
    print("Starting server locally...")
    uvicorn.run("api:app", host="0.0.0.0", port=4000)
