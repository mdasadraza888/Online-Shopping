from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail
from fastapi.responses import JSONResponse
import secrets
from app.core.config import settings
from html import escape

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


async def send_otp_email(email: str, username: str):
    safe_username = escape(username)

    otp = generate_otp()

    msg = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;
                     line-height: 1.6;">
            <h2>Verify Your Email Address 🔐</h2>

            <p>Hi {safe_username},</p>

            <p>
                Thank you for registering with
                <strong>Online Shopping</strong>!
                To complete your registration, please verify your
                email address using the OTP below.
            </p>

            <div style="text-align: center; margin: 25px 0;">
                <p>Your verification code is:</p>
                <h1 style="letter-spacing: 8px; color: #2563eb;">
                    {escape(otp)}
                </h1>
            </div>

            <p>
                <strong>⏳ Important:</strong> This OTP is valid for
                <strong>5 minutes only</strong>. Please do not share
                it with anyone.
            </p>

            <p>
                If you did not create an account with us, you can
                safely ignore this email.
            </p>

            <p>
                Best regards,<br>
                <strong>The Online Shopping Team</strong>
            </p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Verify Your Email - Online Shopping",
        recipients=[email],
        body=msg,
        subtype=MessageType.html,
    )

    fm = FastMail(config=conf)
    await fm.send_message(message=message)

    return otp


async def send_email(email: str, username: str):
    msg = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2>Welcome to Online Shopping, {username}! 🛍️</h2>

            <p>Thank you for registering with <strong>Online Shopping</strong>!
            We're delighted to have you join our community.</p>

            <p>Your account is ready, and you can now explore our latest
            products, discover your favorite styles, and enjoy a seamless
            shopping experience.</p>

            <h3>🎁 Your Welcome Gift</h3>
            <p>Enjoy <strong>10% off your first order!</strong></p>

            <p>
                <strong>Promo Code:</strong>
                <span style="background-color: #f2f2f2; padding: 6px 10px;">
                    WELCOME10
                </span>
            </p>

            <p>Enter the promo code at checkout to redeem your welcome offer,
            subject to the promotion's terms.</p>

            <p>We're excited to be part of your shopping journey!</p>

            <p>
                Happy Shopping!<br>
                <strong>The Online Shopping Team</strong>
            </p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Welcome to Online Shopping! 🎉",
        recipients=[email],
        body=msg,
        subtype=MessageType.html,
    )

    fm = FastMail(config=conf)
    await fm.send_message(message=message)


