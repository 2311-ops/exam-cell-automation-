from rest_framework import serializers
from halltickets.models import Exam, ExamRoom, HallTicket
from marksheets.models import Mark
from students.models import Student


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'name', 'course_code', 'date']


class ExamRoomSerializer(serializers.ModelSerializer):
    exam_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamRoom
        fields = ['id', 'exam', 'exam_name', 'room_number', 'capacity', 'occupied_seats']
    
    def get_exam_name(self, obj):
        return obj.exam.name


class HallTicketSerializer(serializers.ModelSerializer):
    exam_name = serializers.SerializerMethodField()
    course_code = serializers.SerializerMethodField()
    room_number = serializers.SerializerMethodField()
    
    class Meta:
        model = HallTicket
        fields = ['id', 'exam', 'exam_name', 'course_code', 'exam_room', 'room_number', 'seat_no', 'status', 'issue_date', 'email_sent']
    
    def get_exam_name(self, obj):
        return obj.exam.name
    
    def get_course_code(self, obj):
        return obj.exam.course_code
    
    def get_room_number(self, obj):
        return obj.exam_room.room_number if obj.exam_room else None


class MarkSerializer(serializers.ModelSerializer):
    exam_name = serializers.SerializerMethodField()
    course_code = serializers.SerializerMethodField()
    
    class Meta:
        model = Mark
        fields = ['id', 'exam', 'exam_name', 'course_code', 'subject', 'score', 'grade', 'created_at']
    
    def get_exam_name(self, obj):
        return obj.exam.name
    
    def get_course_code(self, obj):
        return obj.exam.course_code


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'username', 'gpa']
