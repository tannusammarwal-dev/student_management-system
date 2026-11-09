
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Course, Mark, Student


# Login Form
class LoginForm(AuthenticationForm):
    pass


# Registration Form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')

        return email


# Course Form
class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['name', 'code', 'duration_months', 'description']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_code(self):
        code = self.cleaned_data['code'].strip().upper()

        qs = Course.objects.filter(owner=self.user, code__iexact=code)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError('You already have a course with this code.' )

        return code


# Student Form
class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['roll_number','first_name','last_name','email','phone', 'gender','date_of_birth','course','admission_date','address', 'is_active'
        ]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        self.fields['course'].queryset = Course.objects.filter(
            owner=user
        )

        self.fields['course'].empty_label = '-- No course --'

    def clean_roll_number(self):
        roll = self.cleaned_data['roll_number'].strip()

        qs = Student.objects.filter(
            owner=self.user,
            roll_number__iexact=roll
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                'A student with this roll number already exists.'
            )

        return roll


# Mark Form
class MarkForm(forms.ModelForm):

    class Meta:
        model = Mark
        fields = ['subject', 'score', 'exam_date']
