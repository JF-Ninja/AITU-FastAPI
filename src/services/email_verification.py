import aiosmtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailService:
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")

    @staticmethod
    async def send_email(to_email: str, verification_code: int) -> None:
        msg = MIMEMultipart()
        msg["From"] = EmailService.sender_email
        msg["To"] = to_email
        msg["Subject"] = "Код верификации"
        text = f"Ваш код верификации: {verification_code}"
        msg.attach(MIMEText(text, "plain"))

        async with aiosmtplib.SMTP(hostname=EmailService.smtp_server, port=EmailService.port) as smtp:
            await smtp.connect()
            await smtp.login(EmailService.sender_email, EmailService.sender_password)
            await smtp.sendmail(EmailService.sender_email, to_email, msg.as_string())
