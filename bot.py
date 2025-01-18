import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.username} started the bot.")
    await update.message.reply_text('Hello! I am bot. Use /menu to see the options.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.username} requested help.")
    await update.message.reply_text('Available commands: /menu')

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.username} accessed the menu.")
    keyboard = [
        [InlineKeyboardButton("Hello", callback_data='button1')],
        [InlineKeyboardButton("Source Code", callback_data='button2')],
        [InlineKeyboardButton("Send Photo", callback_data='button3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose an option:', reply_markup=reply_markup)How are you
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'button1':
        response_text = 'Hello world!!!'
    elif query.data == 'button2':
        response_text = 'https://github.com/Kz-TelegramBot/telegram-bot'
    elif query.data == 'button3':
        response_text = 'Wait...'
        photo_url = 'https://pomf2.lain.la/f/ih8u1243.jpg'
        await query.message.reply_photo(photo=photo_url)
    else:
        response_text = 'Not available.'

    logger.info(f"Outgoing message: {response_text} to user {query.from_user.username}")
    await query.edit_message_text(text=response_text)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    logger.info("Bot is starting...")
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CallbackQueryHandler(handle_callback))

    application.run_polling()
    logger.info("Bot has started.")