import asyncio
import base64
import logging
import time

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import (
    ADMINS,
    FORCE_MSG,
    START_MSG,
    CUSTOM_CAPTION,
    IS_VERIFY,
    VERIFY_EXPIRE,
    SHORTLINK_API,
    SHORTLINK_URL,
    DISABLE_CHANNEL_BUTTON,
    PROTECT_CONTENT,
    AUTO_DELETE_TIME,
    AUTO_DELETE_MSG
)
from helper_func import subscribed, encode, decode, get_messages, get_verify_status, update_verify_status, delete_file
from database.database import add_user, del_user, full_userbase, present_user

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default messages
WAIT_MSG = "Please wait, fetching users..."
REPLY_ERROR = "Reply to a message to broadcast."

#==================== START COMMAND ====================#
@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    track_msgs = []

    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except Exception as e:
            logger.warning(f"Add user failed: {e}")

    verify_status = await get_verify_status(user_id)
    if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
        await update_verify_status(user_id, is_verified=False)

    # Token verification
    if "verify_" in message.text:
        _, token = message.text.split("_", 1)
        if verify_status['verify_token'] != token:
            return await message.reply("Your token is invalid or expired. Click /start to retry.")
        await update_verify_status(user_id, is_verified=True, verified_time=time.time())
        await message.reply(f"Token successfully verified and valid for 12 hours.",
                            reply_markup=None, protect_content=False, quote=True)
        return

    # /start with argument
    if len(message.text) > 7 and verify_status['is_verified']:
        try:
            base64_string = message.text.split(" ", 1)[1]
            decoded_str = await decode(base64_string)
            argument = decoded_str.split("-")
        except Exception as e:
            logger.warning(f"Start argument decode error: {e}")
            return

        # Calculate message IDs
        ids = []
        try:
            if len(argument) == 3:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end+1) if start <= end else list(range(start, end-1, -1))
            elif len(argument) == 2:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
        except Exception as e:
            logger.warning(f"ID calculation error: {e}")
            return

        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            await temp_msg.edit("Something went wrong while fetching messages.")
            logger.error(e)
            return
        await temp_msg.delete()

        # Copy messages and track for auto-delete
        for msg in messages:
            caption = ""
            if CUSTOM_CAPTION and msg.document:
                caption = CUSTOM_CAPTION.format(
                    previouscaption="" if not msg.caption else msg.caption.html,
                    filename=msg.document.file_name
                )
            elif msg.caption:
                caption = msg.caption.html

            reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None

            try:
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                if AUTO_DELETE_TIME > 0:
                    track_msgs.append(copied_msg)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                if AUTO_DELETE_TIME > 0:
                    track_msgs.append(copied_msg)
            except Exception as e:
                logger.warning(f"Error copying message: {e}")

        # Auto-delete messages
        if track_msgs and AUTO_DELETE_TIME > 0:
            delete_msg = await client.send_message(
                chat_id=message.from_user.id,
                text=AUTO_DELETE_MSG.format(time=AUTO_DELETE_TIME)
            )
            asyncio.create_task(delete_file(track_msgs, client, delete_msg))
        return

    # Normal /start without argument
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("About Me", callback_data="about"),
         InlineKeyboardButton("Close", callback_data="close")]
    ])
    await message.reply_text(
        text=START_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=f"@{message.from_user.username}" if message.from_user.username else None,
            mention=message.from_user.mention,
            id=user_id
        ),
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        quote=True
    )

#==================== FORCE SUB (Not joined) ====================#
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [[InlineKeyboardButton("Join Channel", url=client.invitelink)]]
    try:
        buttons.append([InlineKeyboardButton("Try Again", url=f"https://t.me/{client.username}?start={message.command[1]}")])
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=f"@{message.from_user.username}" if message.from_user.username else None,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )

#==================== GET USERS ====================#
@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

#==================== BROADCAST ====================#
@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if not message.reply_to_message:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        return await msg.delete()

    query = await full_userbase()
    broadcast_msg = message.reply_to_message
    total = successful = blocked = deleted = unsuccessful = 0

    pls_wait = await message.reply("<i>Broadcasting message... Please wait</i>")
    for chat_id in query:
        try:
            await broadcast_msg.copy(chat_id)
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await broadcast_msg.copy(chat_id)
            successful += 1
        except UserIsBlocked:
            await del_user(chat_id)
            blocked += 1
        except InputUserDeactivated:
            await del_user(chat_id)
            deleted += 1
        except:
            unsuccessful += 1
        total += 1

    status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""

    await pls_wait.edit_text(status)
