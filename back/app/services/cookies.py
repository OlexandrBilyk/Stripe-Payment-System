from app.core import DEBUG
from fastapi import Response


def set_cookies(res: Response, access_token: str, refresh_token: str):
    secure = not DEBUG

    res.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=60 * 12,
        samesite="none",
        secure=secure,  
        path="/",
    )

    res.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=60 * 60 * 24,
        samesite="none",
        secure=secure,  
        path="/",
    )
