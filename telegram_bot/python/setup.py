from telegram.ext import CommandHandler
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram_bot.python.command_handlers import notify_availability, start, stop, help

import os
from dotenv import load_dotenv

load_dotenv()

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

def setup():
    application = ApplicationBuilder().token(telegram_bot_token).build()
    
    command_handlers = []
    command_handlers.append(CommandHandler('start', start))
    command_handlers.append(CommandHandler('help', help))
    command_handlers.append(CommandHandler('stop', stop))
    command_handlers.append(CommandHandler('checkAvailability', notify_availability))

    for command_handler in command_handlers:
        application.add_handler(command_handler)
    
    application.run_polling()