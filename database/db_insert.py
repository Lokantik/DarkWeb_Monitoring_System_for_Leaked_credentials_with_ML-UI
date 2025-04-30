import sqlite3
   
from logger.custom_logger import log_event

def insert_credential(cred_type, value, source):
    conn = sqlite3.connect('database/leaked_credentials.db')
    c = conn.cursor()
    c.execute('INSERT INTO credentials (type, value, source) VALUES (?, ?, ?)',
              (cred_type, value, source))
    conn.commit()
    conn.close()
    log_event(f"Inserted {cred_type} into database: {value}")

    