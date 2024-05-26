from auth import fake_db as db


def authenticate_user(username: str, password: str):
    user = db.fake_db.get(username)
    if not user or user['password'] != password:
        return False
    return True
