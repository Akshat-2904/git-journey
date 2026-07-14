import uvicorn
from app.app import app
if __name__ == "__main__":
    # Point directly to the app instance object instead of the "main:app" string
    uvicorn.run("main:app", host="127.0.0.1", port=8000)