import requests
import logging
from telegram import Update
from telegram.ext import ContextTypes
from time import sleep 
import os
from dotenv import load_dotenv

load_dotenv()

province = os.getenv("PROVINCE")
welcome_message = True
times_checked_without_availability = 0


async def notify_availability(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global welcome_message
    global times_checked_without_availability

    starting_monitoring = "Starting passport availability detection.. 😎"
    passport_available = "Passport booking is now available! 🤩"
    passport_not_available = "No availability found in the last two hours.. 😭"
    
    while True:
        if welcome_message == True:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=starting_monitoring)
            welcome_message = False
        
        if check_availability() == True:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=passport_available)
            logging.info(passport_available)
            times_checked_without_availability = 0                
        else:
            logging.info("No passport booking availability at the moment")
            times_checked_without_availability = times_checked_without_availability + 1
        
        if times_checked_without_availability == 7200:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=passport_not_available)
            times_checked_without_availability = 0
        sleep(1)

def check_availability():
    url = 'https://www.passaportonline.poliziadistato.it/CittadinoAction.do'
    params = {'codop': 'resultRicercaRegistiProvincia', 'provincia': province}
    headers = {
        'Host': 'www.passaportonline.poliziadistato.it',
        'Cookie': 'AGPID_FE=AGj6aSgKxwrZ9K85KvJTFA$$; JSESSIONID=xsNzlcG3eip8SK1nAEdzvVpB; AGPID=AZ84BZoLxwpyRQFrN/JiaA$$; fontsCssCache=true; spid_domain_jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvYXV0aC5wb2xpemlhZGlzdGF0by5pdCIsImlhdCI6MTY5ODg1ODE5NSwiZXhwIjoxNjk4OTQ0NTk1LCJqdGkiOiJjZWMxMjkxNy01ZmQ0LTRjNjctYWU1NC1kNGRlZGE3ODg1MTciLCJzdWIiOiJhZmMxODUwMmQ0YWU4NjU5NGVmMzFmNTAwYzc5ZGRlYyIsImF1ZCI6ImRvbWFpblwvbHZsLTBcL3NsbyJ9.o5_E3vLDlLgzVAlHQ2ez56eK2Aq5jxdSFJuzI_siWCpHLVvvOQnBtFVXNehksGGE_ig-5n_axu64aBZ1imcgGXN1t6XWCoMZ4B91I2CeaQudz6RpRAGXI-DhXjOpTTBHj1vwa2k95TsapiQkjT4HF3zz6DhQvIE1lbUZFxNP4ObW8LmbesYl7gN8yu5PMfVqjhDnAxNld4CEjvmgVeuYKWVMcYoQ90xwRQv7CHwU4UCl83qlmZKzLbXDCXoiv-k3sgSTw2_KvWqKfAfCJYKdrha7Vwz67J1gIy53mEhWpxh_88Dg_BJNWT0jTS1tg_SpzR2E98IpSMMAXBpH09v8LQ; DWRSESSIONID=7sX5hFrrY0M~UBzVSePk0GQzbFHKNWJRbKo',
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
    return "Non ci sono diponibilità nelle strutture della tua provincia" in response.text
   
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"""Hello {update.effective_user.first_name}!""")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Type /help to list all available commands ")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Type /checkAvailability to start passport availability checking 🧐")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"""See ya, {update.effective_user.first_name}!""")