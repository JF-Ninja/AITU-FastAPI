import aiosmtplib
import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


class EmailService:
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "eserikova22@gmail.com"
    sender_password = "zokthaldgnrnfjtw"

    @staticmethod
    async def send_email(to_email: str, verification_code: int) -> None:
        msg = MIMEMultipart()
        msg["From"] = EmailService.sender_email
        msg["To"] = to_email
        msg["Subject"] = "Код верификации"
        text = f"Ваш код верификации: {verification_code}"
        msg.attach(MIMEText(text, "plain"))

        try:
            smtp = aiosmtplib.SMTP(hostname=EmailService.smtp_server, port=EmailService.port)
            await smtp.connect()
            await smtp.starttls()
            await smtp.login(EmailService.sender_email, EmailService.sender_password)
            await smtp.sendmail(EmailService.sender_email, to_email, msg.as_string())
            await smtp.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")