from rest_framework import serializers
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
