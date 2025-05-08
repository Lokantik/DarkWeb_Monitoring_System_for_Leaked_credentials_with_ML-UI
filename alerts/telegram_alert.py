import requests
from config import TELEGRAM_SETTINGS
from logger.custom_logger import log_event  

def send_telegram_alert(leak):
    token = TELEGRAM_SETTINGS['bot_token']
    chat_id = TELEGRAM_SETTINGS['chat_id']
    message = f'''
    New Leak Detected!
    - Type: {leak['type']}
    - Value: {leak['value']}
    - Source: {leak['source']}
    '''
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"Telegram alert sent to chat_id {chat_id}")
        else:
            print(f"Telegram failed: {response.text}")
    except Exception as e:
        print(f"Telegram error: {e}")
log_event("Telegram alert sent")