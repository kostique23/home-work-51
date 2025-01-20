import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных окружения

class NotificationManager:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.admin_email = os.getenv("ADMIN_EMAIL")

        if not all([self.smtp_server, self.sender_email, self.sender_password, self.admin_email]):
            raise ValueError("В файле .env отсутствуют настройки уведомлений по электронной почте")

    def send_low_balance_notification(self, balance):
        """Отправка уведомления о низком балансе."""
        try:
            msg = MIMEText(f"У вас низкий баланс на OpenRouter: {balance}. Пожалуйста, пополните баланс.", _charset="utf-8")
            msg["Subject"] = "OpenRouter: Низкий баланс"
            msg["From"] = self.sender_email
            msg["To"] = self.admin_email

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                print("Уведомление по email успешно отправлено!")

        except Exception as e:
            print(f"Ошибка отправки email уведомления: {e}")
