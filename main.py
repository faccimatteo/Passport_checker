from log.setup import setup as setup_log
from telegram_bot.python.setup import setup as setup_telegram

def main():
    setup_log()
    setup_telegram()

if __name__ == '__main__':
    main()