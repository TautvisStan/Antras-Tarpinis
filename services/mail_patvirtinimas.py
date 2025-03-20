from itsdangerous import URLSafeTimedSerializer
from config import Config
from flask_mail import Message
from extensions import mail
from config import Config

def generate_token(email):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        email = serializer.loads(
            token, salt=Config.SECURITY_PASSWORD_SALT, max_age=expiration
        )
        return email
    except Exception:
        return False





def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=Config.MAIL_USERNAME
    )
    mail.send(msg)
