from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def send_welcome_email(to_email, username):
    """Send a welcome email when a new user registers"""
    
    subject = "Welcome to Exam Cell Automation"
    context = {'username': username}
    #loads the HTML template and replace username with actual username
    message = render_to_string('email_templates/welcome_email.html', context)
    #create email object and send email 
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [to_email])
    email.content_subtype = "html"
    email.send()
    return True


def send_exam_notification(to_email, exam_name, exam_date):
    """Reusable function to notify users about new exams"""
    subject = "New Exam Notification"
    context = {'exam_name': exam_name, 'exam_date': exam_date}
    message = render_to_string('email_templates/exam_notification.html', context)

    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [to_email])
    email.content_subtype = "html"
    email.send()
    return True
