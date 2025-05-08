import sqlite3

DB_path = r"C:\Users\lokan\Desktop\Dark_Web_Monitoring_System_for_Leaked_Credentials_with-ML&UI\database\leaked_credential.db" 

def search_email(email):
    conn = sqlite3.connect(DB_path)
    c = conn.cursor()
    c.execute("SELECT type, value, source FROM credentials WHERE value = ?", (email,))
    results = c.fetchall()
    conn.close()
    return results
