import os
import logging
from logging.handlers import RotatingFileHandler

# ================= BOT CONFIG =================
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", "31212516"))
API_HASH = os.environ.get("API_HASH", "ccc20df465364045538da8ecf8954992l")

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001925121665"))
OWNER_ID = int(os.environ.get("OWNER_ID", "6645288126"))
PORT = int(os.environ.get("PORT", "8585"))

# Database
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://user:pass@cluster0.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

# Shortener API
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "arolinks.com")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "8d6b2153682ca17a4f89e662199d6b5917893bf0")

# Verification
VERIFY_EXPIRE = int(os.environ.get("VERIFY_EXPIRE", 43200))
IS_VERIFY = os.environ.get("IS_VERIFY", "True")
TUT_VID = os.environ.get("TUT_VID", "https://t.me/+JAdctcMYdSUzZGU1")

# Force Sub Channel
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1003598465147"))

# Auto-delete config
AUTO_DELETE_TIME = int(os.environ.get("AUTO_DELETE_TIME", 180))
AUTO_DELETE_MSG = os.environ.get(
    "AUTO_DELETE_MSG",
    "This file will be automatically deleted in {time} seconds. Please ensure you have saved any necessary content before this time."
)
AUTO_DEL_SUCCESS_MSG = os.environ.get(
    "AUTO_DEL_SUCCESS_MSG",
    "Your file has been successfully deleted. Thank you for using our service. ✅"
)

# Bot behavior
PROTECT_CONTENT = os.environ.get("PROTECT_CONTENT", "False") == "True"
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "False") == "True"
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "This video/Photo/anything is available on the internet. We LeakHubd or its subsidiary channel doesn't produce any of them.")

# Messages
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link.")
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join my Channel/Group to use me\n\nKindly Please join Channel</b>")
WAIT_MSG = "Please wait..."
REPLY_ERROR = "❌ Reply to a message to broadcast it."

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

# Admins
ADMINS = []
for x in (os.environ.get("ADMINS", "1480923991 5069922547 6695586027").split()):
    ADMINS.append(int(x))

ADMINS.append(OWNER_ID)
ADMINS.append(1955406483)

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
