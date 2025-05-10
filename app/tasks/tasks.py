import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery_app
from app.tasks.email_templates import create_booking_confirmation_template


@celery_app.task
def process_pic(
        path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_max = im.resize((1000, 500))
    im_resized_min = im.resize((200, 100))

    im_resized_max.save(f"app/static/images/resized_max_{im_path.name}")
    im_resized_min.save(f"app/static/images/resized_min_{im_path.name}")


@celery_app.task
def send_confirmation_email(
        booking: dict,
        email_to: EmailStr,
):
    msg_content = create_booking_confirmation_template(
        booking,
        email_to,
    )

    with smtplib.SMTP_SSL(
        host=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
    ) as server:
        server.login(user=settings.SMTP_USER, password=settings.SMTP_PASSWORD)
        server.send_message(msg_content)
