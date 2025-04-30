```markdown
# Dark Web Monitoring System for Leaked Credentials

A final-year B.Tech cyber security project that scrapes dark web sources (via TOR) for leaked email addresses and credentials. Users can check via a simple web interface if their email has been compromised.

---

## Features

-  Scrapes dark web forums via TOR proxy
-  Detects leaked emails, usernames, passwords
-  Email + Telegram alerts for leaks
-  Modular architecture for easy updates
-  Simple UI for users to check if their email has been leaked
-  SQLite database for storing leaked data
-  Logging for every run and activity

---

## Project Structure

```
darkweb_monitoring_project/
│
├── app.py                         # Flask Web App
├── config.py                      # Configs for TOR, Email, Telegram
├── requirements.txt               # Python dependencies
│
├── scraping/
│   └── tor_scraper.py             # Scraper with TOR proxy
│
├── extraction/
│   └── pattern_matcher.py         # Regex-based credential extraction
│
├── database/
│   ├── db_setup.py                # Create DB
│   ├── db_insert.py               # Insert into DB
│   └── db_query.py                # Query email from DB
│
├── alerts/
│   ├── email_alert.py             # SMTP-based alerts
│   └── telegram_alert.py          # Telegram bot alerts
│
├── logger/
│   └── custom_logger.py           # Logging utility
│
├── templates/
│   ├── index.html                 # Home page UI
│   └── result.html                # Results page
│
├── static/
│   └── style.css                  # Basic CSS
```

---

## Installation :

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/darkweb-monitoring.git
   cd darkweb-monitoring
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create the database:
   ```bash
   python database/db_setup.py
   ```

5. Start the Flask app:
   ```bash
   python app.py
   ```

---

## Web Interface

- Visit `http://127.0.0.1:5000/`
- Enter an email to check if it has been leaked
- See real-time results from stored dark web data

---

## Testing Dark Web Scraping (Example)

Update `config.py` with working `.onion` URLs and then run:

```python
from scraping.tor_scraper import scrape_dark_web
from extraction.pattern_matcher import extract_credentials
from database.db_insert import insert_credential

url = "http://exampledarkweb.onion/leaks"
soup = scrape_dark_web(url)
if soup:
    text = soup.get_text()
    emails, usernames, passwords = extract_credentials(text)
    for e in emails:
        insert_credential("email", e, url)
```

---

## Configurations

Update the following in `config.py`:
- **TOR** proxy settings
- **Email SMTP** credentials
- **Telegram Bot Token + Chat ID**

---

## Logging

Logs are automatically saved in `logs/run_log.txt`  
Use it to monitor scraping progress, alerts, and database inserts.

---

## Future Scope

- Integrate machine learning for leak pattern prediction
- Real-time alert dashboard
- Scan pastebins and clearnet forums

---

## Author & Credits

**Your Name** – B.Tech Final Year Cyber Security  
Contributors welcome!

---

## Disclaimer

For educational and ethical cybersecurity research only. Do not use on real-world dark web platforms without permission and legal clearance.
```
# Dark_Web_Monitoring_System_for_Leaked_Credentials_with-ML&UI
