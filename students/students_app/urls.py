
from django.urls import path,include
from .import views

urlpatterns = [
   path("",views.dashboard,name='dashboard'),

   # Authentication
   path("register",views.register_user,name='register'),
   path("login",views.login_user,name='login'),
   path("logout/",views.logout_user,name='logout'),

   # Student Management
   path("students",views.students_list,name='students_list'),
   path("students/add",views.students_create,name='students_create'),
   path("students/<int:pk>",views.student_details,name='student_detail'),
   path("students/<int:pk>/edit",views.students_edit,name='students_edit'),
   path("students/<int:pk>/delete",views.students_delete,name='students_delete'),

   # course
   path("courses",views.courses_list,name='courses_list'),
   path("courses/add",views.courses_create,name='courses_create'),
   path("courses/<int:pk>/edit",views.courses_edit,name='courses_edit'),
   path("courses/<int:pk>/delete",views.courses_delete,name='courses_delete'),

   # Marks
   path("marks",views.marks_delete,name='marks_delete'),
]
