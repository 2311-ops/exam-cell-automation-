from rest_framework import serializers
from marksheets.models import Marksheet
from halltickets.models import Exam

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'name', 'description', 'exam_date', 'duration_minutes', 'total_marks']


class MarksheetSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)

    class Meta:
        model = Marksheet
        fields = [
            'id', 'student_username', 'exam', 'marks_obtained', 'total_marks',
            'percentage', 'grade', 'result_status', 'published_at', 'remarks'
        ]
        read_only_fields = ['id', 'percentage', 'grade', 'result_status']
