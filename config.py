import os
import logging
from logging.handlers import RotatingFileHandler

# ==================== BOT CONFIG ==================== #

# Bot token from @BotFather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

# Your API ID & API HASH from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "31212516"))
API_HASH = os.environ.get("API_HASH", "ccc20df465364045538da8ecf8954992l")

# Your database channel ID (where bot stores files)
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001925121665"))

# Owner ID
OWNER_ID = int(os.environ.get("OWNER_ID", "6645288126"))

# Port for webhook / server (Koyeb)
PORT = int(os.environ.get("PORT", "8585"))

# ==================== DATABASE ==================== #
DB_URI = os.environ.get(
    "DATABASE_URL",
    "mongodb+srv://ultroidxTeam:ultroidxTeam@cluster0.gabxs6m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

# ==================== SHORTLINK / TOKEN ==================== #
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "arolinks.com")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "8d6b2153682ca17a4f89e662199d6b5917893bf0")

IS_VERIFY = os.environ.get("IS_VERIFY", "True") == "True"
VERIFY_EXPIRE = int(os.environ.get("VERIFY_EXPIRE", 43200))  # in seconds
TUT_VID = os.environ.get("TUT_VID", "https://t.me/+JAdctcMYdSUzZGU1")

# ==================== AUTO-DELETE FILE SETTINGS ==================== #
AUTO_DELETE_TIME = int(os.environ.get("AUTO_DELETE_TIME", "180"))  # seconds
AUTO_DELETE_MSG = os.environ.get(
    "AUTO_DELETE_MSG",
    "This file will be automatically deleted in {time} seconds. Please save it before deletion."
)
AUTO_DEL_SUCCESS_MSG = os.environ.get(
    "AUTO_DEL_SUCCESS_MSG",
    "Your file has been successfully deleted. ✅"
)

# ==================== FORCE SUBSCRIBE ==================== #
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1003598465147"))
FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE",
    "Hello {first}\n\n<b>You need to join my Channel/Group to use this bot.\nKindly join the channel first!</b>"
)

# ==================== BOT SETTINGS ==================== #
CUSTOM_CAPTION = os.environ.get(
    "CUSTOM_CAPTION",
    "This video/photo is available on the internet. We do not produce any of them."
)

PROTECT_CONTENT = True if os.environ.get("PROTECT_CONTENT", "False") == "True" else False
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "False") == "True"

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# Start message
START_MSG = os.environ.get(
    "START_MESSAGE",
    "Hello {first}\n\nI can store private files in a specified channel and other users can access them via a special link."
)

# Admins
try:
    ADMINS = [int(x) for x in os.environ.get("ADMINS", "1480923991 5069922547 6695586027").split()]
except ValueError:
    raise Exception("Admins list must contain valid integers.")

# Always add owner and your extra admin
ADMINS.append(OWNER_ID)
ADMINS.append(1955406483)  # optional extra admin

# ==================== LOGGING ==================== #
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
