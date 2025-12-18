from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

def send_welcome_email(to_email, username):

    subject = "Welcome to Exam Cell Automation"
    context = {'username': username}
    # render the HTML template
    try:
        message = render_to_string('email_templates/welcome_email.html', context)
    except Exception as e:
        logger.error(f"Failed to render welcome email template: {str(e)}")
        message = f"Welcome to Exam Cell Automation, {username}!"

    from_email = settings.DEFAULT_FROM_EMAIL
    
    logger.info(f"Attempting to send welcome email to {to_email} from {from_email}")
    logger.debug(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    logger.debug(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    logger.debug(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")

    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[to_email],
        )
        email.content_subtype = "html"
        result = email.send(fail_silently=False)
        logger.info(f"Welcome email sent successfully to {to_email} (result: {result})")
        return True
    except Exception as e:
        logger.error(f"Failed to send welcome email to {to_email}: {str(e)}", exc_info=True)
        # Don't let email failures break user registration; return False so caller can log if needed.
        return False

def send_exam_notification(to_email, exam_name, exam_date):
    subject = "New Exam Notification"
    context = {'exam_name': exam_name, 'exam_date': exam_date}
    try:
        message = render_to_string('email_templates/exam_notification.html', context)
    except Exception as e:
        logger.error(f"Failed to render exam notification template: {str(e)}")
        message = f"Exam {exam_name} scheduled for {exam_date}"

    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[to_email],
        )
        email.content_subtype = "html"
        result = email.send(fail_silently=False)
        logger.info(f"Exam notification sent successfully to {to_email} (result: {result})")
        return True
    except Exception as e:
        logger.error(f"Failed to send exam notification to {to_email}: {str(e)}", exc_info=True)
        return False
