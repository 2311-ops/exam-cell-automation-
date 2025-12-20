import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_email_to_admin(request):
    """
    Allow authenticated students to send emails to admin
    """
    try:
        subject = request.data.get('subject', '').strip()
        message = request.data.get('message', '').strip()
        student_email = request.user.email
        student_username = request.user.username

        if not subject or not message:
            return Response({"error": "Subject and message are required"}, status=400)

        if len(subject) > 200:
            return Response({"error": "Subject too long (max 200 characters)"}, status=400)

        if len(message) > 2000:
            return Response({"error": "Message too long (max 2000 characters)"}, status=400)

        # Admin email - you can make this configurable
        admin_email = "madhouse2311.2005@gmail.com"

        # Create email content
        email_subject = f"Student Inquiry: {subject}"
        email_context = {
            'student_username': student_username,
            'student_email': student_email,
            'subject': subject,
            'message': message,
            'timestamp': request.data.get('timestamp', 'N/A')
        }

        try:
            email_body = render_to_string('email_templates/student_to_admin.html', email_context)
        except Exception as e:
            logger.error(f"Failed to render student to admin email template: {str(e)}")
            # Fallback plain text
            email_body = f"""
Student: {student_username} ({student_email})

Subject: {subject}

Message:
{message}
            """

        # Send email to admin
        email = EmailMessage(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [admin_email],
            reply_to=[student_email]  # Allow admin to reply directly to student
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)

        logger.info(f"Student {student_username} sent email to admin: {subject}")

        return Response({"status": "Email sent to admin successfully!"})

    except Exception as e:
        logger.error(f"Failed to send email to admin: {str(e)}")
        return Response({"error": "Failed to send email. Please try again."}, status=500)


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
