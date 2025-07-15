import os
from fastapi import UploadFile, HTTPException, status

AVATAR_UPLOAD_DIR = "avatars"
ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png"}
AVATAR_MAX_SIZE = 2 * 1024 * 1024  # 2MB

# Helper to secure filename (no path traversal)
def secure_filename(filename):
    return os.path.basename(filename.replace("..", ""))

def get_extension(filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    return ext

def is_allowed_extension(filename):
    return get_extension(filename) in ALLOWED_EXTENSIONS

def validate_and_save_avatar(upload_file: UploadFile) -> str:
    # Check file extension/type by header and filename
    extension = get_extension(upload_file.filename)

    if not is_allowed_extension(upload_file.filename):
        raise HTTPException(status_code=415, detail="Unsupported file type. Only JPEG and PNG allowed.")

    # Read header for quick type check
    content_start = upload_file.file.read(10)
    upload_file.file.seek(0)

    if extension in {"jpg", "jpeg"} and not content_start.startswith(b"\xff\xd8"):
        raise HTTPException(status_code=415, detail="Invalid JPEG signature.")
    if extension == "png" and not content_start.startswith(b"\x89PNG"):
        raise HTTPException(status_code=415, detail="Invalid PNG signature.")

    # Limit size
    upload_file.file.seek(0, os.SEEK_END)
    size = upload_file.file.tell()
    upload_file.file.seek(0)
    if size > AVATAR_MAX_SIZE:
        raise HTTPException(status_code=413, detail="Avatar too large (max 2MB).")
    
    # Save with a safe filename
    unique_name = f"avatar_{str(abs(hash(upload_file.filename)))}.{extension}"
    full_path = os.path.join(AVATAR_UPLOAD_DIR, unique_name)
    with open(full_path, "wb") as f:
        contents = upload_file.file.read()
        f.write(contents)
    return unique_name

def get_avatar_url_for_profile(profile: dict):
    if profile.get("avatar_filename"):
        return f"/avatars/{profile['avatar_filename']}"
    return None
