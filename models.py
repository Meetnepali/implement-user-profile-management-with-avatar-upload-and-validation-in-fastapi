from pydantic import BaseModel, Field, constr
from typing import Optional

USERNAME_REGEX = r"^[A-Za-z0-9_\-\.]{3,32}$"
DISPLAY_NAME_REGEX = r"^[A-Za-z\s'\-]{1,64}$"

class UserProfileResponse(BaseModel):
    username: constr(regex=USERNAME_REGEX, min_length=3, max_length=32)
    display_name: constr(min_length=1, max_length=64)
    bio: str = Field(max_length=256)
    avatar_url: Optional[str] = None

class UserProfileUpdate(BaseModel):
    username: constr(regex=USERNAME_REGEX, min_length=3, max_length=32)
    display_name: constr(min_length=1, max_length=64)
    bio: str = Field(max_length=256)

class UserProfileAvatarResponse(BaseModel):
    avatar_url: str
