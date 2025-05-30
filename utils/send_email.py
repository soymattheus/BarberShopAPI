from urllib.parse import urlencode, quote
from dotenv import load_dotenv
import os

from utils.email_service import send_email
from utils.generate_ics import generate_and_save_ics

load_dotenv()

front_base_url = os.getenv('FRONT_URL')

def send_activation_email(email: str, activation_link: str):
    subject = "Welcome to The Barrio Barber!"
    body = f"Hey {email}, welcome to The Barrio Barber!"
    html = f"""
        <h1>Welcome, {email}!</h1>
        <p>Your registration has been successfully completed at <b>The Barrio Barber</b>.</p>
        <p>We are happy to have you with us!</p>
        <p>Click the link below to activate your account and start using our services:</p>
        <a href="{activation_link}">Activate your account</a>
        <p style="margin-top: 20px; color: gray; font-size: 12px;">
            Please do not reply to this email. This is an automated message.
        </p>
    """

    send_email(subject, [email], body, html)

def send_resend_activation_email(email: str, activation_link: str):
    subject = "Complete Your Registration at The Barrio Barber!"
    body = f"Hey {email}, please confirm your account at The Barrio Barber."
    html = f"""
        <h1>Hi, {email}!</h1>
        <p>It looks like you haven't activated your account at <b>The Barrio Barber</b> yet.</p>
        <p>Click the link below to activate your account and start using our services:</p>
        <a href="{activation_link}">Activate your account</a>
        <p>If you did not request this, please ignore this email.</p>
        <p style="margin-top: 20px; color: gray; font-size: 12px;">
            Please do not reply to this email. This is an automated message.
        </p>
    """

    send_email(subject, [email], body, html)

def send_completed_activation_email(email: str):
    subject = "Welcome to The Barrio Barber!"
    body = f"Hey {email}, welcome to The Barrio Barber!"
    html = f"""
        <h1>Welcome, {email}!</h1>
        <p>Your account has been successfully activated at <b>The Barrio Barber</b>.</p>
        <p>We are happy to have you with us!</p>
        <p>Schedule an appointment with us right now and enjoy our services.</p>
        <a href="{front_base_url}">Access your account</a>
        <p style="margin-top: 20px; color: gray; font-size: 12px;">
            Please do not reply to this email. This is an automated message.
        </p>
    """

    send_email(subject, [email], body, html)

def send_password_updated_email(email: str):
    subject = "Your password has been updated - The Barrio Barber"
    body = f"Hey {email}, your password has been successfully updated at The Barrio Barber!"
    html = f"""
        <h1>Password Updated Successfully</h1>
        <p>Hey {email},</p>
        <p>This is a confirmation that your password has been successfully updated at <b>The Barrio Barber</b>.</p>
        <p>If you did not perform this action, please contact our support team immediately.</p>
        <a href="{front_base_url}">Access your account</a>
        <p style="margin-top: 20px; color: gray; font-size: 12px;">
            Please do not reply to this email. This is an automated message.
        </p>
    """

    send_email(subject, [email], body, html)

def send_booking_confirmation_email(email: str, name: str, barber: str, date: str, time: str, service: str, appointment_id: str):
    subject = "Your Appointment is Confirmed - The Barrio Barber"

    # Google Calendar link
    event_title = f"{service} at The Barrio Barber"
    event_description = "Your appointment is confirmed. We look forward to seeing you!"
    event_location = "The Barrio Barber - Your Location Address"
    start_datetime = f"{date}T{time.replace(':', '')}00"
    end_hour = str(int(time.split(":")[0]) + 1).zfill(2)
    end_datetime = f"{date}T{end_hour}{time.split(':')[1]}00"

    params = {
        "action": "TEMPLATE",
        "text": event_title,
        "details": event_description,
        "location": event_location,
        "dates": f"{start_datetime}/{end_datetime}",
    }
    google_calendar_link = f"https://www.google.com/calendar/render?{urlencode(params, quote_via=quote)}"

    # ICS file
    ics_content = generate_and_save_ics(name, date, time, service)
    ics_filename = f"appointment_{appointment_id}.ics"
    with open(ics_filename, "w") as f:
        f.write(ics_content)

    body = f"Hey {name}, your appointment for {service} is confirmed for {date} at {time} at The Barrio Barber."

    html = f"""
        <h1>Hey, {name}!</h1>
        <p>Your appointment for <b>{service}</b> has been <b>confirmed</b> at <b>The Barrio Barber</b>.</p>
        <p><b>Barber:</b> {barber}</p>
        <p><b>Date:</b> {date}</p>
        <p><b>Time:</b> {time}</p>
        <p>We look forward to seeing you!</p>

        <p>
            <a href="{google_calendar_link}" target="_blank"
               style="display: inline-block; padding: 10px 20px; background-color: #4285F4; color: white;
                      text-decoration: none; border-radius: 4px;">
                Add to Google Calendar
            </a>
        </p>

        <p>
            <a href="cid:{ics_filename}"
               style="display: inline-block; padding: 10px 20px; background-color: #34A853; color: white;
                      text-decoration: none; border-radius: 4px;">
                Add to Apple/Outlook Calendar
            </a>
        </p>

        <p>If you need to reschedule, click below:</p>
        <a href="{front_base_url}">Manage Your Appointments</a>

        <p style="margin-top: 20px; color: gray; font-size: 12px;">
            Please do not reply to this email. This is an automated message.
        </p>
    """

    send_email(
        subject,
        [email],
        body,
        html,
        attachments=[(ics_filename, ics_content, "text/calendar")],
    )