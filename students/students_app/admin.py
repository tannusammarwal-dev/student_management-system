from django.contrib import admin
from .models import Course, Mark, Student


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'duration_months', 'owner')
    search_fields = ('code', 'name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'first_name', 'last_name', 'course', 'is_active', 'owner')
    list_filter = ('course', 'is_active', 'gender')
    search_fields = ('roll_number', 'first_name', 'last_name', 'email')


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score', 'exam_date')
