#!/usr/bin/env python
"""
Script to populate the database with test data for the debuguser.
Run with: python manage.py shell -c "exec(open('create_test_data.py').read())"
"""

from django.contrib.auth import get_user_model
from halltickets.models import Exam, ExamRoom, HallTicket
from marksheets.models import Mark
from students.models import Student
from decimal import Decimal

User = get_user_model()

# Get or create the debuguser and their student record
user = User.objects.get(username='debuguser')
student, created = Student.objects.get_or_create(user=user)

# Clear old data
Exam.objects.all().delete()
ExamRoom.objects.all().delete()
HallTicket.objects.all().delete()
Mark.objects.all().delete()

# Create exams
exams = [
    Exam.objects.create(name='Mathematics Final', course_code='MATH-101', date='2025-11-25'),
    Exam.objects.create(name='Physics Midterm', course_code='PHYS-201', date='2025-11-26'),
    Exam.objects.create(name='Chemistry Lab', course_code='CHEM-150', date='2025-11-27'),
]

# Create exam rooms
rooms = [
    ExamRoom.objects.create(exam=exams[0], room_number='A-101', capacity=30, occupied_seats=0),
    ExamRoom.objects.create(exam=exams[1], room_number='B-202', capacity=25, occupied_seats=0),
    ExamRoom.objects.create(exam=exams[2], room_number='C-303', capacity=20, occupied_seats=0),
]

# Create hall tickets (registrations)
for i, room in enumerate(rooms):
    hall_ticket = HallTicket.objects.create(
        student=student,
        exam=room.exam,
        exam_room=room,
        seat_no=5 + i,
        status='confirmed',
        email_sent=True
    )
    # Increment occupied seats
    room.occupied_seats += 1
    room.save()

# Create marks
marks_data = [
    {'exam': exams[0], 'subject': 'Algebra', 'score': 85},
    {'exam': exams[1], 'subject': 'Mechanics', 'score': 92},
    {'exam': exams[2], 'subject': 'Organic Chemistry', 'score': 78},
]

for mark_data in marks_data:
    Mark.objects.create(
        student=student,
        exam=mark_data['exam'],
        subject=mark_data['subject'],
        score=Decimal(str(mark_data['score']))
    )

print("✓ Created 3 exams")
print("✓ Created 3 exam rooms")
print("✓ Created 3 hall tickets (registrations) for debuguser")
print("✓ Created 3 marks for debuguser")
print("\nDashboard is now populated with test data!")

