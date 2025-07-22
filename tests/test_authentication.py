from datetime import timedelta
from src.utils.authentication import (
    register_user,
    authenticate_user,
    create_access_token,
    verify_token
)

def test_register_auth_and_token(tmp_path, monkeypatch):
    user_db = tmp_path / "users.json"
    monkeypatch.setenv("USER_DB_PATH", str(user_db))

    # Register user and authenticate
    assert register_user("alice", "password123")
    assert authenticate_user("alice", "password123")

    # Generate and verify access token
    token = create_access_token("alice", expires_delta=timedelta(minutes=5))
    claims = verify_token(token)

    assert claims is not None
    assert claims.get("username") == "alice"
