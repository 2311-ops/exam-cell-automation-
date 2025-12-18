from django.contrib.auth import get_user_model
from rest_framework import serializers

from halltickets.models import Exam, HallTicket
from marksheets.models import Marksheet
from students.models import StudentExamRegistration

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "is_staff",
            "is_superuser",
            "is_active",
            "date_joined",
            "last_login",
        ]
        read_only_fields = ["id", "date_joined", "last_login"]


class AdminExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = [
            "id",
            "name",
            "description",
            "exam_date",
            "duration_minutes",
            "total_marks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class AdminStudentExamRegistrationSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source="student.username", read_only=True)
    exam_name = serializers.CharField(source="exam.name", read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        source="student", queryset=User.objects.all(), write_only=True
    )
    exam_id = serializers.PrimaryKeyRelatedField(
        source="exam", queryset=Exam.objects.all(), write_only=True
    )

    class Meta:
        model = StudentExamRegistration
        fields = [
            "id",
            "student_username",
            "exam_name",
            "student_id",
            "exam_id",
            "registered_at",
            "is_approved",
        ]
        read_only_fields = ["id", "registered_at"]


class AdminHallTicketSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source="student.username", read_only=True)
    exam_name = serializers.CharField(source="exam.name", read_only=True)

    class Meta:
        model = HallTicket
        fields = [
            "id",
            "student",
            "student_username",
            "exam",
            "exam_name",
            "roll_number",
            "seat_number",
            "room_number",
            "invigilator_name",
            "issued_at",
        ]
        read_only_fields = ["id", "issued_at"]


class AdminMarksheetSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source="student.username", read_only=True)
    exam_name = serializers.CharField(source="exam.name", read_only=True)

    class Meta:
        model = Marksheet
        fields = [
            "id",
            "student",
            "student_username",
            "exam",
            "exam_name",
            "marks_obtained",
            "total_marks",
            "percentage",
            "grade",
            "result_status",
            "published_at",
            "remarks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "percentage",
            "grade",
            "result_status",
            "created_at",
            "updated_at",
        ]
