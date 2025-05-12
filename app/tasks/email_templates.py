from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr,
):
    email = EmailMessage()

    email['Subject'] = 'Booking Confirmation'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to

    email.set_content(
        f"""
        <h1>Confirm Your Booking</h1>
        <p>Your booked hotel with dates: {booking['date_from']} to {booking['date_to']}</p>
""",
        subtype='html',
    )

    return email
