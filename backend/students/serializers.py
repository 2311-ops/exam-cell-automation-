from rest_framework import serializers
from students.models import StudentExamRegistration
from halltickets.models import Exam

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'name', 'description', 'exam_date', 'duration_minutes', 'total_marks']


class StudentExamRegistrationSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    exam_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = StudentExamRegistration
        fields = ['id', 'exam', 'exam_id', 'registered_at', 'is_approved']
        read_only_fields = ['id', 'registered_at', 'is_approved']
