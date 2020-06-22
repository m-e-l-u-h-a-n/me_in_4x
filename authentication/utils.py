import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config


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
        print(e.message)

