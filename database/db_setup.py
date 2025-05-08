import sqlite3
   
DB_path = r"C:\Users\lokan\Desktop\Dark_Web_Monitoring_System_for_Leaked_Credentials_with-ML&UI\database\leaked_credential.db"   

def init_db():
    conn = sqlite3.connect(DB_path)
    c = conn.cursor()
    
    # Table for leaked credentials
    c.execute('''CREATE TABLE IF NOT EXISTS credential (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    value TEXT,
                    source TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    password TEXT,
                    notify_email INTEGER DEFAULT 1,
                    notify_telegram INTEGER DEFAULT 0
                )''')
    
    conn.commit()
    conn.close()

def ensure_chat_id_column():
    conn = sqlite3.connect(DB_path)
    c = conn.cursor()

    # Check if 'chat_id' column exists
    c.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in c.fetchall()]

    if 'chat_id' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN chat_id TEXT')
        print("chat_id column added.")
    else:
        print("chat_id column already exists.")
    conn.close()

    

if __name__ == '__main__':
    init_db()
    ensure_chat_id_column()