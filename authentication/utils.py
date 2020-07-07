import os
import gzip
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config
from django.contrib.auth.models import User

def send_email(recipient, subject, content):
    message = Mail(
        from_email=config('DEFAULT_FROM_EMAIL', cast=str),
        to_emails=recipient,
        subject=subject,
        html_content=content,
    )
    try:
        sg = SendGridAPIClient(config('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(content)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


def delete_with_email(email):
    if len(email) > 0:
        try:
            user = User.objects.get(email=email)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return "No user with given credentials"
        user.delete()
        return "Account deleted successfully"
    else:
        return "No user with given credentials"


def delete_with_username(username):
    if len(username) > 0:
        try:
            user = User.objects.get(username=username)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return "No user with given credentials"
        user.delete()
        return "Account deleted successfully"
    else:
        return "No user with given credentials"
