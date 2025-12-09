from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from students.models import StudentExamRegistration
from students.serializers import StudentExamRegistrationSerializer, ExamSerializer
from halltickets.models import HallTicket, Exam
from halltickets.serializers import HallTicketSerializer
from marksheets.models import Marksheet
from marksheets.serializers import MarksheetSerializer


class RegisterExamView(APIView):
    """Register a student for an exam"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Register current user for an exam"""
        exam_id = request.data.get('exam_id')
        
        if not exam_id:
            return Response(
                {'error': 'exam_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        exam = get_object_or_404(Exam, id=exam_id)
        
        # Check if already registered
        existing = StudentExamRegistration.objects.filter(
            student=request.user,
            exam=exam
        ).first()
        
        if existing:
            return Response(
                {'message': 'Already registered for this exam'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create registration
        registration = StudentExamRegistration.objects.create(
            student=request.user,
            exam=exam
        )

        serializer = StudentExamRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """Get all exams the student is registered for"""
        registrations = StudentExamRegistration.objects.filter(student=request.user)
        serializer = StudentExamRegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewAvailableExamsView(APIView):
    """View all available exams"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all available exams"""
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewHallTicketView(APIView):
    """View hall tickets for a student"""
    permission_classes = [IsAuthenticated]

    def get(self, request, exam_id=None):
        """Get hall ticket(s) for student"""
        if exam_id:
            # Get hall ticket for specific exam
            hall_ticket = get_object_or_404(
                HallTicket,
                student=request.user,
                exam_id=exam_id
            )
            serializer = HallTicketSerializer(hall_ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Get all hall tickets for student
            hall_tickets = HallTicket.objects.filter(student=request.user)
            serializer = HallTicketSerializer(hall_tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ViewMarksheetView(APIView):
    """View marksheets for a student"""
    permission_classes = [IsAuthenticated]

    def get(self, request, exam_id=None):
        """Get marksheet(s) for student"""
        if exam_id:
            # Get marksheet for specific exam
            marksheet = get_object_or_404(
                Marksheet,
                student=request.user,
                exam_id=exam_id
            )
            serializer = MarksheetSerializer(marksheet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Get all marksheets for student
            marksheets = Marksheet.objects.filter(student=request.user)
            serializer = MarksheetSerializer(marksheets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
