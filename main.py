import os
from fastapi import FastAPI, UploadFile, File, HTTPException, status, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
from models import (
    UserProfileResponse,
    UserProfileUpdate,
    UserProfileAvatarResponse,
)
from utils import (
    validate_and_save_avatar,
    ALLOWED_EXTENSIONS,
    AVATAR_UPLOAD_DIR,
    AVATAR_MAX_SIZE,
    get_avatar_url_for_profile,
    secure_filename
)

app = FastAPI()

# ensure avatar directory exists
os.makedirs(AVATAR_UPLOAD_DIR, exist_ok=True)

# In-memory user profile. In production, this would be a database.
user_profile = {
    "username": "johndoe",
    "display_name": "John Doe",
    "bio": "Hello, I'm John!",
    "avatar_filename": None,  # str or None
}

# Serve avatar files statically
app.mount("/avatars", StaticFiles(directory=AVATAR_UPLOAD_DIR), name="avatars")

@app.get("/profile", response_model=UserProfileResponse)
def get_profile():
    return {
        "username": user_profile["username"],
        "display_name": user_profile["display_name"],
        "bio": user_profile["bio"],
        "avatar_url": get_avatar_url_for_profile(user_profile),
    }

@app.put("/profile", response_model=UserProfileResponse)
def update_profile(upd: UserProfileUpdate):
    user_profile["username"] = upd.username
    user_profile["display_name"] = upd.display_name
    user_profile["bio"] = upd.bio
    return {
        "username": user_profile["username"],
        "display_name": user_profile["display_name"],
        "bio": user_profile["bio"],
        "avatar_url": get_avatar_url_for_profile(user_profile),
    }

@app.post("/profile/avatar", response_model=UserProfileAvatarResponse)
def upload_avatar(file: UploadFile = File(...)):
    try:
        filename = validate_and_save_avatar(file)
        user_profile["avatar_filename"] = filename
        avatar_url = f"/avatars/{filename}"
        return {"avatar_url": avatar_url}
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid upload.")

# The /avatars/{filename} endpoint is handled via StaticFiles.
# Extra catching for files not found (FastAPI StaticFiles returns 404 automatically).
