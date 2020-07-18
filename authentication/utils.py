import os
import gzip
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config
from django.contrib.auth.models import User
import magic

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


def validateSize(f):
    """
        2.5MB - 2621440
        5MB - 5242880
        10MB - 10485760
        20MB - 20971520
        50MB - 5242880
        100MB 104857600
        250MB - 214958080
        500MB - 429916160
    """
    maxUploadSize = 104852760
    try:
        if f.size > maxUploadSize:
            print(f.name, " file size exceeded")
            return False
        return True
    except AttributeError:
        print(f.name, "Attribute Error")
        return False


def validate_file_type(f):
    valid_mime_types = ['image/jpg', 'image/png', 'image/gif', 'image/jpeg', 'application/pdf', 'application/vnd.oasis.opendocument.text',
                        'text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']

    valid_file_extensions = ['.jpg', '.png', '.gif',
                             '.jpeg', '.pdf', '.odt', '.txt', '.docx', 'doc']
    ext = os.path.splitext(f.name)[1]
    if ext.lower() not in valid_file_extensions:
        print(f.name, " Invalid file extensions")
        return False
    file_mime_type = magic.from_buffer(f.read(1024), mime=True)
    if file_mime_type not in valid_mime_types:
        print(f.name, " Invalid mime types")
        return False
    return True
