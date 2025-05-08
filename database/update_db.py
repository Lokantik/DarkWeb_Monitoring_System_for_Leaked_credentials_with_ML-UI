import sqlite3

DB_path = r"C:\Users\lokan\Desktop\Dark_Web_Monitoring_System_for_Leaked_Credentials_with-ML&UI\database\leaked_credential.db"

conn = sqlite3.connect(DB_path)
c = conn.cursor()

# Update existing rows to set status as 'Unknown' if it's NULL
c.execute("UPDATE credential SET status = 'Unknown' WHERE status IS NULL;")

conn.commit()
conn.close()

print("✅ Updated existing rows with 'Unknown' status.")
