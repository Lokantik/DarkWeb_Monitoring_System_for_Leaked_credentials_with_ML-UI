import socks
import socket
import requests
from bs4 import BeautifulSoup
from config import TOR_PROXY, TOR_PORT
from ml_model.predict import predict_leak
from logger.custom_logger import log_event
   
socks.set_default_proxy(socks.SOCKS5, TOR_PROXY, TOR_PORT)
socket.socket = socks.socksocket
 

def scrape_dark_web(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        log_event(f"Starting scan for URL: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        log_event("Scraping successful. Content extracted.")
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        
        if predict_leak(text):
            print(f"[ML] Potential leak detected on: {url}")
            
        return soup    
       
    except Exception as e:
        log_event(f"Failed to scrape {url}: {e}")
        return None
 