from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from halltickets.models import Exam, ExamRoom, HallTicket
from halltickets.serializers import ExamSerializer, ExamRoomSerializer, HallTicketSerializer
from students.models import Student


class ExamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]


class ExamRoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExamRoom.objects.all()
    serializer_class = ExamRoomSerializer
    permission_classes = [IsAuthenticated]


class HallTicketViewSet(viewsets.ModelViewSet):
    serializer_class = HallTicketSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        return HallTicket.objects.filter(student=student)
    
    def create(self, request, *args, **kwargs):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = Student.objects.create(user=request.user)
        
        exam_id = request.data.get('exam')
        if HallTicket.objects.filter(student=student, exam_id=exam_id).exists():
            return Response(
                {'detail': 'Already registered for this exam'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            exam = Exam.objects.get(id=exam_id)
            room = ExamRoom.objects.filter(exam=exam).first()
            
            if not room:
                room = ExamRoom.objects.create(
                    exam=exam,
                    room_number=f"Room-{exam.id}",
                    capacity=30,
                    occupied_seats=0
                )
            
            if room.occupied_seats >= room.capacity:
                return Response(
                    {'detail': 'Room is full'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            seat_no = room.occupied_seats + 1
            hall_ticket = HallTicket.objects.create(
                student=student,
                exam=exam,
                exam_room=room,
                seat_no=seat_no,
                status='confirmed',
                email_sent=True
            )
            
            room.occupied_seats += 1
            room.save()
            
            serializer = self.get_serializer(hall_ticket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exam.DoesNotExist:
            return Response(
                {'detail': 'Exam not found'},
                status=status.HTTP_404_NOT_FOUND
            )
