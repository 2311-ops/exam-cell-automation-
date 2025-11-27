from rest_framework import serializers
<<<<<<< HEAD
from marksheets.models import Mark


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
=======
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
>>>>>>> 53a8404ef9bfe451dbb0d667faf5fbc46ccafefa
