import os
import logging
from logging.handlers import RotatingFileHandler

# Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

# API ID & Hash
APP_ID = int(os.environ.get("APP_ID", "31212516"))
API_HASH = os.environ.get("API_HASH", "ccc20df465364045538da8ecf8954992l")

# DB Channel ID
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001925121665"))

# Owner ID
OWNER_ID = int(os.environ.get("OWNER_ID", "6645288126"))

# Port
PORT = os.environ.get("PORT", "8585")

# MongoDB
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

# Shortlink system
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "arolinks.com")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "")
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', 21600))  # 6 hours in seconds
IS_VERIFY = os.environ.get("IS_VERIFY", "True") == "True"
TUT_VID = os.environ.get("TUT_VID", "https://t.me/+JAdctcMYdSUzZGU1")

# Auto-delete configuration
AUTO_DELETE_TIME = int(os.environ.get("AUTO_DELETE_TIME", "180"))
AUTO_DELETE_MSG = os.environ.get(
    "AUTO_DELETE_MSG",
    "This file will be automatically deleted in {time} seconds. Please save it."
)
AUTO_DEL_SUCCESS_MSG = os.environ.get(
    "AUTO_DEL_SUCCESS_MSG",
    "Your file has been successfully deleted. ✅"
)

# Force subscription
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1003598465147"))
FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE",
    "Hello {first}, please join my Channel to use the bot!"
)

# Bot behavior
START_MSG = os.environ.get(
    "START_MESSAGE",
    "Hello {first}!\nI can store your files securely."
)
CUSTOM_CAPTION = os.environ.get(
    "CUSTOM_CAPTION",
    "This content is from the internet. We are not the original creator."
)
PROTECT_CONTENT = os.environ.get("PROTECT_CONTENT", "False") == "True"
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "False") == "True"

# Admins
ADMINS = [int(x) for x in os.environ.get("ADMINS", "1480923991 5069922547 6695586027").split()]
ADMINS.append(OWNER_ID)

# Logging
LOG_FILE_NAME = "filesharingbot.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
