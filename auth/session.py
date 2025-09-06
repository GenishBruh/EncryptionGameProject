CURRENT_USER = None

def set_current_user(username: str | None):
    global CURRENT_USER
    CURRENT_USER = username if username else "test"

def get_current_user() -> str | None:
    return CURRENT_USER if CURRENT_USER else "test"