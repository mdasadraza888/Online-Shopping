from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail
from fastapi.responses import JSONResponse
import secrets
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


def generate_otp():

    otp = secrets.randbelow(1_000_000)

    return f"{otp:06d}"


async def send_email(email: str):
    otp = generate_otp()
    msg = f"Your otp for email verification {otp}\nThis otp is valid for just 5 min.\nTHANK YOU."
    message = MessageSchema(
        subject="Account verification",
        recipients=[email],
        body=msg,
        subtype=MessageType.html
    )

    fm = FastMail(config=conf)
    await fm.send_message(message=message)

    return otp
