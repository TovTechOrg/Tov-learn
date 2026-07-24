# send_report.py
import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header
from dotenv import load_dotenv

load_dotenv()

# Load credentials from .env
SMTP_SERVER = os.getenv("SMTP_SERVER") # e.g., "smtp.gmail.com"
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") # App password for Gmail

def send_summary_email(processed_count, recipient_email):
    """Sends a summary email about the lead classification process."""
    
    subject = "סיכום תהליך סיווג לידים"
    body = f"הושלם בהצלחה סיווג של {processed_count} לידים."

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = EMAIL_SENDER
    msg['To'] = recipient_email

    try:
        print(f"מתחבר לשרת {SMTP_SERVER}...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, [recipient_email], msg.as_string())
        print(f"מייל סיכום נשלח בהצלחה אל {recipient_email}")
    except Exception as e:
        print(f"שגיאה בשליחת המייל: {e}")

# דוגמת שימוש (ניתן לשלב עם סקריפט אחר)
if __name__ == "__main__":
    send_summary_email(processed_count=50, recipient_email="gilbaram.de@gmail.com")