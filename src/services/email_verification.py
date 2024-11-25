import smtplib
import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


class EmailService:
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")

    @staticmethod
    async def send_email(to_email: str, verification_code: int) -> None:
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login("eserikova22@gmail.com", "zokthaldgnrnfjtw")
        msg = MIMEMultipart()
        msg["From"] = "eserikova22@gmail.com"
        msg["To"] = to_email
        msg["Subject"] = "Код верификации"
        text = f"Ваш код верификации: {verification_code}"
        msg.attach(MIMEText(text, "plain"))
        smtp_server.sendmail("eserikova22@gmail.com", to_email, msg.as_string())
        smtp_server.quit()

