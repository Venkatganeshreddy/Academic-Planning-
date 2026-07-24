"""Local chat-history persistence for the chat page.

ChatGPT-style: a sidebar list of past conversations that survives restarts. Persists to a
single JSON file — fine for LOCAL / single-user use. On the shared Streamlit Cloud deploy there
is no login and the filesystem is wiped per redeploy, so persistence is OFF there (the chat page
falls back to session-only) — otherwise every visitor would share one history. True per-user
cloud history needs auth + a real store, which this app doesn't have.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_PATH = os.path.join(ROOT, "data", "chat_history.json")


def _persist_enabled():
    """On locally, OFF on Streamlit Cloud (shared FS, no login). `AIP_CHAT_HISTORY=0/1` overrides."""
    override = os.environ.get("AIP_CHAT_HISTORY")
    if override is not None:
        return override.strip().lower() in ("1", "true", "yes", "on")
    # Streamlit Cloud mounts the repo under /mount/src/... — treat that as the shared cloud runtime.
    return "/mount/src" not in ROOT.replace(os.sep, "/")


PERSIST = _persist_enabled()


def load_chats():
    """The saved non-empty chats (creation order), or [] if none / persistence off."""
    if not PERSIST or not os.path.exists(HISTORY_PATH):
        return []
    try:
        with open(HISTORY_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def save_chats(chats):
    """Best-effort write of the given chats; never raises into the UI."""
    if not PERSIST:
        return
    try:
        os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
        with open(HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(chats, f, ensure_ascii=False, indent=1)
    except OSError:
        pass
