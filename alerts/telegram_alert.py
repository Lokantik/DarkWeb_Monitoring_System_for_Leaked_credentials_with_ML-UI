import requests
from config import TELEGRAM_SETTINGS
from logger.custom_logger import log_event  

def send_telegram_alert(message):
    token = TELEGRAM_SETTINGS['bot_token']
    chat_id = TELEGRAM_SETTINGS['chat_id']
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)
log_event("Telegram alert sent") 
   