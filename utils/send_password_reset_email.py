from utils.email_service import send_email

def send_password_reset_email(email, reset_link):
    subject = "Reset your password - The Barrio Barber"
    body = f"""
        Hi {email},

        We received a request to reset your password for your account at The Barrio Barber.

        Click the link below to reset your password:
        {reset_link}

        If you didn't request this, please ignore this email.

        The Barrio Barber Team.
    """

    html = f"""
        <h2>Password Reset Request</h2>
        <p>Hi <b>{email}</b>,</p>
        <p>We received a request to reset your password for your account at <b>The Barrio Barber</b>.</p>
        <p>Click the link below to reset your password:</p>
        <a href="{reset_link}" style="display: inline-block; padding: 10px 20px; background-color: #000; color: #fff; text-decoration: none; border-radius: 4px;">
            Reset Your Password
        </a>
        <p>If you did not request this, please ignore this email.</p>
        <hr />
        <p style="margin-top: 20px; color: gray; font-size: 12px;">
            Please do not reply to this email. This is an automated message from <b>The Barrio Barber</b>.
        </p>
    """

    send_email(subject, [email], body, html)
