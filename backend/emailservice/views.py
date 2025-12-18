import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import send_welcome_email
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


@api_view(['POST'])
def send_test_email(request):
    email = request.data.get('email')
    username = request.data.get('username', 'TestUser')

    send_welcome_email(email, username)

    return Response({"status": "Email sent successfully!"})


def send_exam_notification(to_email, exam_name, exam_date):
    subject = "New Exam Notification"
    context = {
        'exam_name': exam_name,
        'exam_date': exam_date
    }

    message = render_to_string('email_templates/exam_notification.html', context)

    try:
        email = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
        )
        email.content_subtype = "html"  # HTML email
        email.send(fail_silently=False)
        return True

    except Exception as e:
        logger.error(f"Failed to send exam notification to {to_email}: {str(e)}")
        return False
