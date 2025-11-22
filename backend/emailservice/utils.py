from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

def send_welcome_email(to_email, username):

    subject = "Welcome to Exam Cell Automation"
    context = {'username': username}
    # render the HTML template
    message = render_to_string('email_templates/welcome_email.html', context)

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER or 'webmaster@localhost'
    
    logger.info(f"Attempting to send welcome email to {to_email} from {from_email}")
    logger.debug(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    logger.debug(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")

    try:
        email = EmailMessage(subject, message, from_email, [to_email])
        email.content_subtype = "html"
        email.send(fail_silently=False)
        logger.info(f"Welcome email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send welcome email to {to_email}: {str(e)}")
        # Don't let email failures break user registration; return False so caller can log if needed.
        return False

def send_exam_notification(to_email, exam_name, exam_date):
    subject = "New Exam Notification"
    context = {'exam_name': exam_name, 'exam_date': exam_date}
    message = render_to_string('email_templates/exam_notification.html', context)

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER or 'webmaster@localhost'

    try:
        email = EmailMessage(subject, message, from_email, [to_email])
        email.content_subtype = "html"
        email.send(fail_silently=False)
        return True
    except Exception:
        return False
