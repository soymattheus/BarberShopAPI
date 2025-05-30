from flask_mail import Message
from extensions import mail

def send_email(subject, recipients, body, html=None, attachments=None):
    try:
        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body,
            html=html
        )

        if attachments:
            for attachment in attachments:
                filename, data, mimetype = attachment
                msg.attach(filename, mimetype, data)

        mail.send(msg)
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False
