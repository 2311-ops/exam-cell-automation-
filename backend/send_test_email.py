import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','examcell.settings')
import django
django.setup()
from emailservice.utils import send_welcome_email
if __name__ == '__main__':
    to = 'zeinabahgat@gmail.com'
    username = 'zeina_test'
    print('Sending welcome email to', to)
    ok = send_welcome_email(to, username)
    print('SEND_RESULT:', ok)
