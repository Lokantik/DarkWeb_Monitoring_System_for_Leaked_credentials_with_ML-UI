import sqlite3
DB_path = r"C:\Users\lokan\Desktop\Dark_Web_Monitoring_System_for_Leaked_Credentials_with-ML&UI\database\leaked_credential.db" 
from logger.custom_logger import log_event

def insert_credential(cred_type, value, source):
    conn = sqlite3.connect(DB_path)
    c = conn.cursor()
    c.execute('INSERT INTO credentials (type, value, source) VALUES (?, ?, ?)',
              (cred_type, value, source))
    conn.commit()
    conn.close()
    log_event(f"Inserted {cred_type} into database: {value}")

    