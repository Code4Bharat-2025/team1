import os

# You can set these as environment variables or hardcode them here (not recommended for secrets)
BASE_URL = os.getenv("SWIFTCHAT_BASE_URL", "https://v1-api.swiftchat.ai")
BOT_ID = os.getenv("SWIFTCHAT_BOT_ID", "0247309708745990")
AUTH_TOKEN = os.getenv("SWIFTCHAT_AUTH_TOKEN", "21bda582-e8d0-45bc-bb8b-a5c6c555d176")
PORT = int(os.getenv("APP_PORT", 5000))
