import logging
import os
import pyrogram # Make sure pyrogram is imported

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# --- Configuration loaded directly from environment variables ---
# These are the variables you MUST set in Render's environment settings.

# Telegram Bot API Token
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
if not TG_BOT_TOKEN:
    logger.error("TG_BOT_TOKEN environment variable not set. Bot cannot start.")
    exit(1) # Exit if essential variable is missing

# Telegram API ID
# This should be an integer. Use a default of 0 and validate.
try:
    APP_ID = int(os.environ.get("APP_ID", "0"))
    if APP_ID == 0:
        raise ValueError("APP_ID cannot be 0. Please set it correctly.")
except (ValueError, TypeError):
    logger.error("APP_ID environment variable is missing or invalid. Bot cannot start.")
    exit(1)

# Telegram API Hash
API_HASH = os.environ.get("API_HASH")
if not API_HASH:
    logger.error("API_HASH environment variable not set. Bot cannot start.")
    exit(1)

# Download Location for temporary files
DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./downloads/")

# Authorized Users (for bot access control)
# Expects a comma-separated string of user IDs (e.g., "123456789,987654321")
# Initialize as an empty set if not provided, then add the hardcoded ID.
AUTH_USERS_ENV = os.environ.get("AUTH_USERS", "")
AUTH_USERS = set()
if AUTH_USERS_ENV:
    try:
        AUTH_USERS = set(int(x.strip()) for x in AUTH_USERS_ENV.split(',') if x.strip())
    except ValueError:
        logger.warning("AUTH_USERS environment variable contains non-integer values. Ignoring them.")

# Add your specific hardcoded user ID.
# This ensures 861055237 is always an authorized user.
AUTH_USERS.add(861055237)

# --- End Configuration ---


if __name__ == "__main__":
    # Create download directory if it doesn't exist
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
        logger.info(f"Created download directory: {DOWNLOAD_LOCATION}")

    plugins = dict(
        root="plugins"
    )

    # Initialize the Pyrogram client with environment variables
    app = pyrogram.Client(
        "RenameBot",  # Session name for Pyrogram
        bot_token=TG_BOT_TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        plugins=plugins
    )

    logger.info("Starting bot...")
    app.run() # This starts the bot and keeps it running
    logger.info("Bot stopped.")

