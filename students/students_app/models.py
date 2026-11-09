from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MaxValueValidator, MinValueValidator, RegexValidator
from django.urls import reverse
from django.utils import timezone 


class Course(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='courses')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    duration_months = models.PositiveIntegerField(default=6,validators=[MinValueValidator(1)])
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        unique_together = ('owner', 'code')

    def __str__(self):
        return f'{self.code} - {self.name}'

class Student(models.Model):

    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    owner = models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='students')
    roll_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=16, blank=True,
        validators=[ RegexValidator(r'^\+?\d{7,15}$','Enter a valid phone number (7-15 digits).')
        ]
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    date_of_birth = models.DateField(null=True, blank=True)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL, related_name='students')
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    admission_date = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['roll_number']
        unique_together = ('owner', 'roll_number')

    def __str__(self):
        return f'{self.roll_number} - {self.full_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    @property
    def initials(self):
        return f'{self.first_name[:1]}{self.last_name[:1]}'.upper()

    def get_absolute_url(self):
        return reverse('student_detail', args=[self.pk])    



class Mark(models.Model):

    student = models.ForeignKey( Student, on_delete=models.CASCADE,related_name='marks' )
    subject = models.CharField(max_length=100)
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(0),MaxValueValidator(100)]
    )

    exam_date = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ['-exam_date', '-id']

    def __str__(self):
        return f'{self.student.full_name} - {self.subject}: {self.score}'

    @property
    def grade(self):
        for limit, letter in ((90, 'A+'), (80, 'A'), (70, 'B'), (60, 'C'), (50, 'D')):
            if self.score >= limit:
                return letter

        return 'F'