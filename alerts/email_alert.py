import smtplib
from email.mime.text import MIMEText
from config import EMAIL_SETTINGS
from logger.custom_logger import log_event
   
def send_email_alert(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SETTINGS['sender']
    msg['To'] = EMAIL_SETTINGS['receiver']
       
    with smtplib.SMTP(EMAIL_SETTINGS['smtp_server'], EMAIL_SETTINGS['smtp_port']) as server:
        server.starttls()
        server.login(EMAIL_SETTINGS['sender'], EMAIL_SETTINGS['password'])
        server.sendmail(EMAIL_SETTINGS['sender'], EMAIL_SETTINGS['receiver'], msg.as_string())
log_event("Email alert sent")