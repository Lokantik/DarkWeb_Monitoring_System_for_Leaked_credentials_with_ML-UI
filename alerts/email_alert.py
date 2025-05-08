import smtplib
from email.mime.text import MIMEText
from config import EMAIL_SETTINGS
from logger.custom_logger import log_event

# --- Email alert ---
def send_email_alert(to_email, leak):
    subject = "New Leak Detected for You!"
    body = f'''
    Hi,

    We detected a new leak:
    - Type: {leak['type']}
    - Value: {leak['value']}
    - Source: {leak['source']}

    Please take immediate action if needed.

    Stay safe,
    Dark Web Monitoring Team
    '''

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'your_email@example.com'  # CHANGE THIS
    msg['To'] = to_email

    try:
        with smtplib.SMTP(EMAIL_SETTINGS['smtp_server'], EMAIL_SETTINGS['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_SETTINGS['sender'], EMAIL_SETTINGS['password'])
            server.sendmail(EMAIL_SETTINGS['sender'], EMAIL_SETTINGS['receiver'], msg.as_string())
        print(f"Email alert sent to {to_email}")
    except Exception as e:
        print(f"Email failed to {to_email}: {e}")

log_event("Email alert sent")