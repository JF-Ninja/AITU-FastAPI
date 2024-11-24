import aiosmtplib
import smtplib
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
        msg = MIMEMultipart()
        msg["From"] = EmailService.sender_email
        msg["To"] = to_email
        msg["Subject"] = "Код верификации"
        text = f"Ваш код верификации: {verification_code}"
        msg.attach(MIMEText(text, "plain"))
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Убедитесь, что соединение защищено
                server.login(EmailService.sender_email, EmailService.sender_password)
                server.sendmail(EmailService.sender_email, to_email, msg.as_string())
                print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")

