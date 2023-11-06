import requests
import logging
from telegram import Update
from telegram.ext import ContextTypes
from time import sleep 
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

PROVINCE = os.getenv("PROVINCE")
AGPID_FE = os.getenv("AGPID_FE")
JSESSIONID = os.getenv("JSESSIONID")
AGPID = os.getenv("AGPID")
SPID_DOMAIN_JWT = os.getenv("SPID_DOMAIN_JWT")


welcome_message = True
times_checked_without_availability = 0
passport_booking_available = False
last_time_available = 'never'
starting_monitoring = "Starting passport availability detection.. 😎"
passport_availability_message = "Passport booking is now available! 🤩"
passport_ended_availability_message = "Passport booking is not available anymore 😱"
passport_not_available = "No availability found in the last two hours.. 😭"

async def notify_availability(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    """
    Notify the user if passport booking is available
    """
    
    global PROVINCE 
    global AGPID_FE
    global JSESSIONID
    global AGPID
    global SPID_DOMAIN_JWT

    global welcome_message
    global times_checked_without_availability
    global passport_booking_available
    global last_time_available 
    global starting_monitoring
    global passport_ended_availability_message
    global passport_not_available

    while True:
        # Send welcome notification on first message
        if welcome_message == True:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=starting_monitoring)
            welcome_message = False
        
        if check_availability() == True:
            # Sends notification if passport is available just the first time
            if passport_booking_available is not True:
                passport_booking_available = True
                last_time_available = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                await context.bot.send_message(chat_id=update.effective_chat.id, text=passport_availability_message)   
                times_checked_without_availability = times_checked_without_availability + 1             
        else:
            # Notify if passport is not available anymore
            if passport_booking_available is True: 
                passport_booking_available = False
                times_checked_without_availability = 0
                await context.bot.send_message(chat_id=update.effective_chat.id, text=passport_ended_availability_message)
            else: 
                times_checked_without_availability = times_checked_without_availability + 1
            
        # Log passport availability and last time available everytime
        logging.info(f""" {{ "available_for_booking": {str(passport_booking_available)}, "last_time_available": {last_time_available} }}""")

        # If no booking has been found in two hours, notify the user
        if times_checked_without_availability == 360:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=passport_not_available)
            times_checked_without_availability = 0
        
        sleep(20)

def check_availability():
    
    """
    Function performing API polling to check passport availability
    """

    logfile = open("log.html", "w")
    
    url = 'https://www.passaportonline.poliziadistato.it/CittadinoAction.do'
    params = {'codop': 'resultRicercaRegistiProvincia', 'provincia': PROVINCE}
    headers = {
        'Host': 'www.passaportonline.poliziadistato.it',
        'Cookie': f"""AGPID_FE={AGPID_FE}; \
            JSESSIONID={JSESSIONID}; \
            AGPID={AGPID}; \
            spid_domain_jwt={SPID_DOMAIN_JWT};""",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Sec-Gpc': '1',
        'Te': 'trailers',
        'Connection': 'close',
    }

    response = requests.get(url, params=params, headers=headers)
    logfile.write(response.text)
    logfile.close()
    return "<td headers=\"disponibilita\">Si</td>" in response.text
   
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"""Hello {update.effective_user.first_name}!""")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Type /help to list all available commands ")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Type /checkAvailability to start passport availability checking 🧐")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"""See ya, {update.effective_user.first_name}!""")