import os
import yt_dlp
from telegram import ParseMode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re
import logging
from telegram.utils.helpers import mention_html
import pymongo
import time

LOGS_GROUP_ID = -1002854086015
OWNER_ID = 6663845789
# Store the bot's start time  
BOT_START_TIME = time.time()  

mongo_url = "mongodb+srv://Cenzo:Cenzo123@cenzo.azbk1.mongodb.net/"
client = pymongo.MongoClient(mongo_url)
db = client['cenzo_db']
users_collection = db['users']
chats_collection = db['chats']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def add_user(user_id: int) -> None:
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id})


def add_chat(chat_id: int) -> None:
    if not chats_collection.find_one({"chat_id": chat_id}):
        chats_collection.insert_one({"chat_id": chat_id})


def get_users_count() -> int:
    return users_collection.count_documents({})


def get_chats_count() -> int:
    return chats_collection.count_documents({})


def download_video(url) -> str:
    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'postprocessors': [
            {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}
        ],
        'merge_output_format': 'mp4',
        'socket_timeout': 60,
        'http_chunk_size': 10 * 1024 * 1024,
        'max_filesize': 5 * 1024 * 1024 * 1024,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(video_info)


def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat = update.message.chat
  
    # Add user and chat to MongoDB
    add_user(user.id)
    add_chat(chat.id)

    message = f" <b>𝖭𝖾𝗐 𝖴𝗌𝖾𝗋 𝖲𝗍𝖺𝗋𝗍𝖾𝖽 𝗍𝗁𝖾 𝖻𝗈𝗍</b>\n"
    message += f"𝖴𝗌𝖾𝗋: {mention_html(user.id, user.first_name)}\n"
    message += f"𝖯𝗋𝗈𝖿𝗂𝗅𝖾: <a href='tg://user?id={user.id}'>𝖫𝗂𝗇𝗄</a>\n"
    if chat.type != 'private':
        message += f" Group: {chat.title} ({chat.id})"
        if chat.username:
            message += f" - <a href='https://t.me/{chat.username}'>Link</a>"
    context.bot.send_message(LOGS_GROUP_ID, message, parse_mode='HTML')

    bot_username = context.bot.get_me().username
    keyboard = [
        [
            InlineKeyboardButton("𝖡𝗈𝗍 𝖴𝗉𝖽𝖺𝗍𝖾𝗌", url="https://t.me/alcyonebots"),
            InlineKeyboardButton("𝖡𝗈𝗍 𝖲𝗎𝗉𝗉𝗈𝗋𝗍", url="https://t.me/alcyone_support")
        ],
        [
            InlineKeyboardButton("𝖠𝖽𝖽 𝗆𝖾 𝗍𝗈 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉𝗌!!", url=f"https://t.me/{bot_username}?startgroup=true")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    image_url = "https://i.ibb.co/9sH98zC/file-248.jpg"
    
    update.message.reply_photo(
        photo=image_url,
        caption=(
          "𝗛𝗶 𝘁𝗵𝗲𝗿𝗲 👋🏻\n"
          "𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝗍𝗈 𝗩𝗶𝗱𝗲𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿 𝗕𝗼𝘁 𝗯𝘆 𝗔𝗹𝗰𝘆𝗼𝗻𝗲, 𝗒𝗈𝗎𝗋 𝗀𝗈-𝗍𝗈 𝖻𝗈𝗍 𝖿𝗈𝗋 𝖽𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝗁𝗂𝗀𝗁-𝗊𝗎𝖺𝗅𝗂𝗍𝗒 𝖼𝗈𝗇𝗍𝖾𝗇𝗍 𝖿𝗋𝗈𝗆 𝖸𝗈𝗎𝖳𝗎𝖻𝖾 𝖺𝗇𝖽 𝖨𝗇𝗌𝗍𝖺𝗀𝗋𝖺𝗆!!🎬\n"
          "𝗛𝗼𝘄 𝗱𝗼𝗲𝘀 𝗶𝘁 𝘄𝗼𝗿𝗸?\n"
          "≡ 𝖩𝗎𝗌𝗍 𝗌𝖾𝗇𝖽 𝗆𝖾 𝖺 𝗅𝗂𝗇𝗄 𝖺𝗇𝖽 𝖨'𝗅𝗅 𝖽𝗈 𝗍𝗁𝖾 𝗋𝖾𝗌𝗍 𝗈𝖿 𝗍𝗁𝖾 𝗍𝗁𝗂𝗇𝗀'𝗌!\n"
          "⩉ 𝖳𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍, 𝗆𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝗒𝗈𝗎'𝗋𝖾 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝖻𝖾𝖽 𝗍𝗈 𝗈𝗎𝗋 𝗈𝖿𝖿𝗂𝖼𝗂𝖺𝗅 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝖺𝗇𝖽 𝗌𝗎𝗉𝗉𝗈𝗋𝗍 𝖼𝗁𝖺𝗍\n"
          "✥ 𝖫𝖾𝗍'𝗌 𝖦𝖾𝗍 𝖲𝗍𝖺𝗋𝗍𝖾𝖽!!"
        ),
        reply_markup=reply_markup
    )


def stats(update: Update, context: CallbackContext) -> None:  
    if update.message.from_user.id != OWNER_ID:  
        update.message.reply_text("🚫 *𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝗎𝗍𝗁𝗈𝗋𝗂𝗓𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.*", parse_mode=ParseMode.MARKDOWN)  
        return  

    # Calculate uptime  
    uptime_seconds = int(time.time() - BOT_START_TIME)  
    uptime = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))  

    # Calculate ping  
    start_time = time.time()  
    update.message.reply_text("𝖢𝗁𝖾𝖼𝗄𝗂𝗇𝗀 𝗉𝗂𝗇𝗀...", parse_mode=ParseMode.MARKDOWN)  
    ping = round((time.time() - start_time) * 1000, 2)  # Convert to milliseconds  

    # Get total users and chats  
    user_count = get_users_count()  
    chat_count = get_chats_count()  

    update.message.reply_text(f"*𝖡𝗈𝗍 𝖲𝗍𝖺𝗍𝗂𝗌𝗍𝗂𝖼𝗌*\n\n"  
                              f"*𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌:* `{user_count}`\n"  
                              f"*𝖳𝗈𝗍𝖺𝗅 𝖢𝗁𝖺𝗍𝗌:* `{chat_count}`\n"  
                              f"*𝖴𝗉𝗍𝗂𝗆𝖾:* `{uptime}`\n"  
                              f"*𝖯𝗂𝗇𝗀:* `{ping} ms`",  
                              parse_mode=ParseMode.MARKDOWN)


def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    if is_valid_url(url):
        try:
            file_path = download_video(url)

            keyboard = [
                [
                    InlineKeyboardButton("𝖡𝗈𝗍 𝖴𝗉𝖽𝖺𝗍𝖾𝗌", url="https://t.me/alcyonebots"),
                    InlineKeyboardButton("𝖡𝗈𝗍 𝖲𝗎𝗉𝗉𝗈𝗋𝗍", url="https://t.me/alcyone_support")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            with open(file_path, 'rb') as video_file:
                update.message.reply_video(video_file, reply_markup=reply_markup)

            os.remove(file_path)
        except Exception as e:
            update.message.reply_text(f'Error: {str(e)}')
    elif update.message.chat.type != 'private':
        return
    else:
        update.message.reply_text("𝖯𝗅𝖾𝖺𝗌𝖾 𝗌𝖾𝗇𝖽 𝖺 𝗏𝖺𝗅𝗂𝖽 𝖸𝗈𝗎𝖳𝗎𝖻𝖾 𝗈𝗋 𝖨𝗇𝗌𝗍𝖺𝗀𝗋𝖺𝗆 𝗅𝗂𝗇𝗄!!")


def is_valid_url(text: str) -> bool:
    youtube_pattern = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')

    instagram_pattern = re.compile(
        r'(https?://)?(www\.)?(instagram)\.com/(p|reel|tv)/.+')

    return bool(youtube_pattern.match(text) or instagram_pattern.match(text))


def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')
  

def broadcast(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != OWNER_ID:
        update.message.reply_text("🚫 *𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝗎𝗍𝗁𝗈𝗋𝗂𝗓𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.*", parse_mode=ParseMode.MARKDOWN)
        return

    chats_collection = db["chats"]
    chats = chats_collection.find()

    if update.message.reply_to_message:
        message = update.message.reply_to_message
        send_function = lambda chat_id: context.bot.forward_message(chat_id, update.message.chat_id, message.message_id)
    else:
        message_text = " ".join(context.args)
        if not message_text:
            update.message.reply_text("*Usage:* `/broadcast <message>` or reply to a message with `/broadcast`", parse_mode=ParseMode.MARKDOWN)
            return
        send_function = lambda chat_id: context.bot.send_message(chat_id, message_text, parse_mode=ParseMode.MARKDOWN)

    total_users, success_count, fail_count, deleted_accounts = 0, 0, 0, 0
    start_time = time.time()

    for chat in chats:
        chat_id = chat['chat_id']
        total_users += 1
        try:
            send_function(chat_id)
            success_count += 1
        except Exception as e:
            if "user is deactivated" in str(e) or "deleted" in str(e):
                deleted_accounts += 1
            fail_count += 1

    elapsed_time = round(time.time() - start_time, 2)

    update.message.reply_text(
        f"*𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖲𝗎𝗆𝗆𝖺𝗋𝗒*\n\n"
        f"*𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌:* `{total_users}`\n"
        f"*𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅:* `{success_count}`\n"
        f"*𝖥𝖺𝗂𝗅𝖾𝖽:* `{fail_count}`\n"
        f"*𝖣𝖾𝗅𝖾𝗍𝖾𝖽 𝖠𝖼𝖼𝗈𝗎𝗇𝗍𝗌:* `{deleted_accounts}`\n"
        f"*𝖳𝗂𝗆𝖾 𝖳𝖺𝗄𝖾𝗇:* `{elapsed_time} sec`",
        parse_mode=ParseMode.MARKDOWN
    )

def main() -> None:
    updater = Updater("7488772903:AAHSrE1HMUGMOL89x5P3HGeDGgPpUa89424", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CommandHandler("broadcast", broadcast)) 
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
