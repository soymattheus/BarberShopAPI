from utils.email_service import send_email

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
