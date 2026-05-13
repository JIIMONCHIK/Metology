from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user as auth_get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    return auth_get_current_user(token, db)


def get_current_user_optional(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        return auth_get_current_user(token, db)
    except HTTPException:
        return None


def role_required(required_role: str):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role != required_role and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user

    return role_checker
