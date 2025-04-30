import re
   
from logger.custom_logger import log_event

def extract_credentials(text):
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    usernames = re.findall(r"(?<=Username: )\w+", text)
    passwords = re.findall(r"(?<=Password: )\S+", text)
    log_event(f"Found {len(emails)} emails, {len(usernames)} usernames, {len(passwords)} passwords.")
    return emails, usernames, passwords
