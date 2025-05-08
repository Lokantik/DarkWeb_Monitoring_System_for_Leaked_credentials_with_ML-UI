import socks
import socket
import requests
from bs4 import BeautifulSoup
from config import TOR_PROXY, TOR_PORT
from ml_model.predict import predict_leak
from extraction.pattern_matcher import extract_credentials
from logger.custom_logger import log_event

# Setup TOR proxy
socks.set_default_proxy(socks.SOCKS5, TOR_PROXY, TOR_PORT)
socket.socket = socks.socksocket

def scrape_dark_web(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    leaks_found = []

    try:
        log_event(f"Starting scan for URL: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        log_event("Scraping successful. Content extracted.")

        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()

        # Run ML prediction on scraped text
        prediction, confidence = predict_leak(text)
        log_event(f"[ML] Prediction: {prediction}, Confidence: {confidence}%")

        if prediction == 1:
            print(f"[ML] Potential leak detected ({confidence}% confidence) on: {url}")

            # Extract credentials using pattern matcher
            emails, usernames, passwords = extract_credentials(text)
            log_event(f"Extracted {len(emails)} emails, {len(usernames)} usernames, {len(passwords)} passwords.")

            # Convert to leak dicts
            for email in emails:
                leaks_found.append({
                    'type': 'email',
                    'value': email,
                    'source': url
                })
            for username in usernames:
                leaks_found.append({
                    'type': 'username',
                    'value': username,
                    'source': url
                })
            for password in passwords:
                leaks_found.append({
                    'type': 'password',
                    'value': password,
                    'source': url
                })
        else:
            log_event("No leak detected by ML.")

    except Exception as e:
        log_event(f"Failed to scrape {url}: {e}")

    return leaks_found
