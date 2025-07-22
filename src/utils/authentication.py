# src/utils/authentication.py

"""
authentication.py

Handles user registration, authentication, and JWT access tokens.
Requires:
  - Environment variables:
      JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
  - passlib and PyJWT installed.
"""

import os
import json
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

import jwt
from passlib.context import CryptContext

USER_DB_PATH = os.getenv("USER_DB_PATH", "users.json")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_this_secret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _load_users() -> Dict[str, Any]:
    """Load user database or return empty dict if unavailable."""
    if not os.path.exists(USER_DB_PATH):
        return {}
    try:
        with open(USER_DB_PATH, "r", encoding="utf-8") as file_in:
            data = json.load(file_in)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, FileNotFoundError, PermissionError):
        return {}


def _save_users(users: Dict[str, Any]) -> None:
    """Persist user database to disk."""
    try:
        with open(USER_DB_PATH, "w", encoding="utf-8") as file_out:
            json.dump(users, file_out, indent=2)
    except PermissionError:
        pass


def register_user(username: str, password: str) -> bool:
    """
    Register a new user.
    Returns False if username exists, True on success.
    """
    users = _load_users()
    if username in users:
        return False
    hashed = pwd_context.hash(password)
    users[username] = {
        "hashed_password": hashed,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    _save_users(users)
    return True


def authenticate_user(username: str, password: str) -> bool:
    """
    Verify username/password.
    Returns True if credentials match.
    """
    users = _load_users()
    record = users.get(username)
    if not record:
        return False
    stored_hash = record.get("hashed_password", "")
    return pwd_context.verify(password, stored_hash)


def create_access_token(username: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token for a given user.
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {"sub": username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify JWT.
    Returns payload dict on success, None on failure/expiry.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            return None
        return {"username": username}
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


if __name__ == "__main__":
    # Demo
    user, pwd = "alice", "S3cr3t!"
    registered = register_user(user, pwd)
    print("Registered:", registered)
    auth_ok = authenticate_user(user, pwd)
    print("Authenticated:", auth_ok)
    if auth_ok:
        tok = create_access_token(user)
        print("Token:", tok)
        print("Verified payload:", verify_token(tok))
