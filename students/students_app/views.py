from django.db.models.aggregates import Avg
from django.http import request
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import logout,login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.urls import reverse
from .models import Course, Student, Mark
from .forms import  RegisterForm , LoginForm, StudentForm, StudentForm  
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q  


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
@login_required(login_url='login')
def students_list(request):
    q = request.GET.get('q', '').strip()
    course_id = request.GET.get('course', '').strip()
    status = request.GET.get('status', '').strip()

    students = Student.objects.filter(owner=request.user).select_related('course')
    if q:
        students = students.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(roll_number__icontains=q) | Q(email__icontains=q))
    if course_id.isdigit():
        students = students.filter(course_id=int(course_id))
    if status == 'active':
        students = students.filter(is_active=True)
    elif status == 'inactive':
        students = students.filter(is_active=False)

    page_obj = Paginator(students, 8).get_page(request.GET.get('page'))
    params = request.GET.copy()
    params.pop('page', None)

    return render(request, 'student_list.html', {
        'page_obj': page_obj,
        'courses': Course.objects.filter(owner=request.user),
        'q': q, 'course_id': course_id, 'status': status,
        'querystring': params.urlencode(),
    })

    
@login_required(login_url='login')
def students_create(request):
    form = StudentForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        student = form.save(commit=False)
        student.owner = request.user
        student.save()
        messages.success(request, f'Student "{student.full_name}" added.')
        return redirect('student_detail', pk=student.pk)
    return render(request, 'student_form.html', {'form': form, 'title': 'Add Student'})


@login_required(login_url='login')
def student_details(request, pk):
     student = get_object_or_404(
        Student,
        pk=pk,
        owner=request.user)

     return render(request, "student_details.html", {'student': student})

    
@login_required(login_url='login')
def students_edit(request, pk):
    student = get_object_or_404(Student, pk=pk, owner=request.user)
    form = StudentForm(request.POST or None, instance=student, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Student "{student.full_name}" updated.')
        return redirect('student_detail', pk=student.pk)
    return render(request, 'student_form.html', {'form': form, 'title': 'Edit Student'})


@login_required(login_url='login')
def students_delete(request, pk):
    student = get_object_or_404(Student, pk=pk, owner=request.user)
    if request.method == 'POST':
        name = student.full_name
        student.delete()
        messages.success(request, f'Student "{name}" deleted.')
        return redirect('students_list')
    return render(request, 'confirm_delete.html', {
        'object_name': student.full_name, 'kind': 'student',
        'cancel_url': reverse('student_detail', args=[student.pk]),
        'warning': 'All marks of this student will also be deleted.',
    })


# course
@login_required(login_url='login')
def courses_list(request):
    q = request.GET.get('q', '').strip()
    courses = Course.objects.filter(owner=request.user).annotate(student_count=Count('students'))
    if q:
        courses = courses.filter(Q(name__icontains=q) | Q(code__icontains=q))
    return render(request, 'course_list.html', {'courses': courses, 'q': q})
     
         
@login_required(login_url='login')
def courses_create(request):
    return render(request,"courses/courses_create.html")


@login_required(login_url='login')
def courses_edit(request, pk):
    return render(request,"courses/courses_edit.html")  


@login_required(login_url='login')
def courses_delete(request, pk):
    return render(request,"courses/courses_delete.html")


# marks
@login_required(login_url='login')
def marks_delete(request):
    return render(request,"marks/marks_delete.html")
