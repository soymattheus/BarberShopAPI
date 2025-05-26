from flask_mail import Message
from extensions import mail

def send_email(subject, recipients, body, html=None):
    try:
        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body,
            html=html
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False
