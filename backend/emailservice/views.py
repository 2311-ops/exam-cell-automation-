from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import send_welcome_email

@api_view(['POST'])
def send_test_email(request):
    #get email and username from request data
    email = request.data.get('email')
    username = request.data.get('username', 'TestUser')
    #call the utility function to send email
    send_welcome_email(email, username)
    return Response({"status": "Email sent successfully!"})
