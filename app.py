from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from database.user_db import create_user, get_user_by_email, get_user_by_id
from database.db_setup import init_db
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from ml_model.predict import predict_leak
from alerts.email_alert import send_email_alert
from alerts.telegram_alert import send_telegram_alert
from scraping.tor_scraper import scrape_dark_web
from config import TARGET_URLS

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Use a strong secret key

DB_path = r"C:\Users\lokan\Desktop\Dark_Web_Monitoring_System_for_Leaked_Credentials_with-ML&UI\database\leaked_credential.db" 

# Init DB
init_db()

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class
class User(UserMixin):
    def __init__(self, id, email, notify_email, notify_telegram):
        self.id = id
        self.email = email
        self.notify_email = notify_email
        self.notify_telegram = notify_telegram


# User loader
@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_id(user_id)
    if user_data:
        return User(user_data[0], user_data[1], user_data[3], user_data[4])
    return None


# Routes

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        if create_user(email, hashed_password):
            return redirect(url_for('login'))
        return "User already exists or error occurred."
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = get_user_by_email(email)
        if user_data and check_password_hash(user_data[2], password):
            user_obj = User(user_data[0], user_data[1], user_data[3], user_data[4])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        return "Invalid credentials!"
    return render_template('login.html')


# Route: Dashboard (updated)
@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect(DB_path)
    c = conn.cursor()
    c.execute('SELECT * FROM credential WHERE value = ?', (current_user.email,))
    leaks = c.fetchall()
    conn.close()
    return render_template('dashboard.html', leaks=leaks)

@app.route('/check_email', methods=['POST'])
@login_required
def check_email():
    email = request.form['credential']

    # Run ML prediction
    predicted_label, confidence = predict_leak(email)
    predicted_label_text = "Likely Leaked" if predicted_label == 1 else "Safe"

    # Check if email is already saved
    conn = sqlite3.connect(DB_path)
    c = conn.cursor()
    c.execute("SELECT * FROM credential WHERE value = ?", (email,))
    exists = c.fetchone()

    if not exists:
        c.execute(
            'INSERT INTO credential (type, value, source, status) VALUES (?, ?, ?, ?)',
            ('email', email, 'checked_by_user', predicted_label_text)
        )

        conn.commit()

    conn.close()

    # Show result as flash message
    flash(f"ML Prediction: {predicted_label_text} ({confidence}% confidence). Leak {'found in DB.' if exists else 'not found yet, monitoring started.'}")

    return redirect(url_for('dashboard'))


# Route: Update Notification Settings
@app.route('/update_notifications', methods=['POST'])
@login_required
def update_notifications():
    notify_email = 1 if request.form.get('notify_email') else 0
    notify_telegram = 1 if request.form.get('notify_telegram') else 0
    conn = sqlite3.connect(DB_path)
    c = conn.cursor()
    c.execute('UPDATE users SET notify_email = ?, notify_telegram = ? WHERE id = ?',
              (notify_email, notify_telegram, current_user.id))
    conn.commit()
    conn.close()
    flash("Notification settings updated.")
    return redirect(url_for('dashboard'))


# Route: Add Credential
@app.route('/add_credential', methods=['POST'])
@login_required
def add_credential():
    credential = request.form['credential']
    conn = sqlite3.connect(DB_path)
    c = conn.cursor()
    c.execute('INSERT INTO credential (type, value, source) VALUES (?, ?, ?)',
              ('manual', credential, 'user_added'))
    conn.commit()
    conn.close()
    flash("Credential added for monitoring.")
    return redirect(url_for('dashboard'))

def periodic_scrape():
    print("Running periodic scrape...")
    for url in TARGET_URLS:
        print(f"Scraping: {url}")
        leaks = scrape_dark_web(url)
        conn = sqlite3.connect(DB_path)
        c = conn.cursor()

        for leak in leaks:
            # Check if leak already exists
            c.execute('SELECT * FROM credential WHERE value = ? AND source = ?', (leak['value'], leak['source']))
            if not c.fetchone():
                # New leak: insert into DB
                c.execute(
                    'INSERT INTO credential (type, value, source) VALUES (?, ?, ?)',
                    (leak['type'], leak['value'], leak['source'])
                )
                conn.commit()
                print(f"New leak saved: {leak['value']}")

                # Find user(s) to alert
                c.execute('SELECT * FROM users WHERE email = ?', (leak['value'],))
                user = c.fetchone()
                if user:
                    user_id = user[0]
                    user_email = user[1]
                    notify_email = user[3]
                    notify_telegram = user[4]

                    # Prepare leak data for alerts
                    leak_data = {
                        'type': leak['type'],
                        'value': leak['value'],
                        'source': leak['source']
                    }

                    if notify_email:
                        send_email_alert(user_email, leak_data)

                    if notify_telegram:
                        send_telegram_alert(leak_data)

        conn.close()
    
# APScheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(periodic_scrape, 'interval', hours=6)  # Change 'hours=6' to test faster like 'minutes=1'
scheduler.start()

# Shutdown gracefully
atexit.register(lambda: scheduler.shutdown())

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
