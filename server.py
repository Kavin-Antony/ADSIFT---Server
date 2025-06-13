""" gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 server:app """
""" ngrok http 8000 --domain=goshawk-musical-liger.ngrok-free.app """
import subprocess
import json
import os
import atexit
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
# import atexit
# from pydantic import BaseModel

# class OTPRequest(BaseModel):
#     user_id: str
#     otp: str

# def cleanup():
#     print("Cleaning up before exit...")

# atexit.register(cleanup)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/fm')
def deliver():
    file_path = "output.txt"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        with open(file_path, "r") as file:
            data = json.load(file) 
        return data
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format in file")


USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

@app.post("/signup/")
def signup(
    user_id: str = Form(...),
    username: str = Form(...),
    password: str = Form(...)
):
    users = load_users()

    if user_id in users:
        return {"success": False, "message": "User already registered."}

    users[user_id] = {
        "username": username,
        "password": password
    }
    save_users(users)

    return {"success": True, "message": "User registered successfully."}

@app.post("/login/")
def login(user_id: str = Form(...), password: str = Form(...)):
    users = load_users()
    user = users.get(user_id)

    if not user or user["password"] != password:
        return {"success": False, "message": "Incorrect Password or User ID"}

    return {"success": True, "message": "User login successful"}
























# otp_store: dict[str, str] = {}

# @app.post("/send-otp/")
# def send_otp(user_id: str):
#     otp = "123456"  
#     otp_store[user_id] = otp
#     print(otp_store)
#     return {"message": "OTP sent successfully."}

# @app.post("/verify-otp/")
# def verify_otp(request: OTPRequest):
#     saved_otp = otp_store.get(request.user_id)
#     if not saved_otp:
#         raise HTTPException(status_code=404, detail="OTP not found or expired")

#     if request.otp != saved_otp:
#         raise HTTPException(status_code=400, detail="Invalid OTP")

#     del otp_store[request.user_id]

#     return {"message": "OTP verified successfully"}



# Entry point for running with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
