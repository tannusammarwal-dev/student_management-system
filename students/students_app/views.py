from django.db.models.aggregates import Avg
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import logout,login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Course, Student, Mark
from django.db.models import Count
from .forms import  RegisterForm , LoginForm    

# Create your views here.

 # Authentication

def register_user(request): 
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        form =  RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request,'register sucessfull 👍!')
            return redirect('login.html')

        else:
            messages.error(request,"registration failed please try again!")
            return render(request,"register.html",{'form':form})
    else:
        form = RegisterForm() 
        return render(request,"register.html",{'form': form})


def login_user(request):    
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, "Login successfully!")
            return redirect('dashboard')

        else:
            messages.error(
                request, "Invalid username or password!"
            )
    else:
        form = LoginForm()

    return render(
        request, 'login.html', {'form': form}
    )

def logout_user(request):
    logout(request)
    messages.success(request,"you have been logged out")
    return redirect('login')


# dashboard 
@login_required(login_url='login')
def dashboard(request):
    students = Student.objects.filter(owner=request.user)
    courses = Course.objects.filter(owner=request.user)

    course_stats = list(courses.annotate(student_count=Count('students')).order_by('-student_count', 'name')[:6])
    top = max((c.student_count for c in course_stats), default=0)
    for course in course_stats:
        course.percent = int(course.student_count * 100 / top) if top else 0

    context = {
        'total_students': students.count(),
        'active_students': students.filter(is_active=True).count(),
        'total_courses': courses.count(),
        'average_score': Mark.objects.filter(student__owner=request.user).aggregate(a=Avg('score'))['a'],
        'unassigned': students.filter(course__isnull=True).count(),
        'course_stats': course_stats,
        'recent_students': students.select_related('course').order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html', context)
    
    
   


# Student Management
def students_list(request):
    return render(request,"students/students_list.html")

def students_create(request):
    return render(request,"students/students_create.html")

def students_details(request, pk):
    return render(request,"students/students_details.html")

def students_edit(request, pk):
    return render(request,"students/students_edit.html")

def students_delete(request, pk):
    return render(request,"students/students_delete.html")

# course
def courses_list(request):
    return render(request,"courses/courses_list.html")      

def courses_create(request):
    return render(request,"courses/courses_create.html")

def courses_edit(request, pk):
    return render(request,"courses/courses_edit.html")  

def courses_delete(request, pk):
    return render(request,"courses/courses_delete.html")


# marks
def marks_delete(request):
    return render(request,"marks/marks_delete.html")
