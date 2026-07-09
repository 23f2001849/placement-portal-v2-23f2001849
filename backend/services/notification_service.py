import requests
from config import GOOGLE_CHAT_WEBHOOK_URL
from extensions import db
from models.system import NotificationLog


def send_google_chat(message: str) -> bool:
    if not GOOGLE_CHAT_WEBHOOK_URL:
        print("No webhook URL configured")
        return False
    try:
        response = requests.post(
            GOOGLE_CHAT_WEBHOOK_URL,
            json={'text': message},
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return False


def notify_and_log(notification_type: str, recipient: str, message: str):
    success = send_google_chat(message)
    log = NotificationLog(
        notification_type=notification_type,
        recipient=recipient,
        message=message,
        status='sent' if success else 'failed'
    )
    db.session.add(log)
    db.session.commit()