from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='home'),
    path('login_student/', Login_Student, name='login_student'),
    path('register_student/', Register, name='register'),
    path('login_committee/', Login_Committee, name='login_committee'),
    path('home_student/', Home_Student, name='home_student'),
    path('home_admin/', Home_Admin, name='home_admin'),
    path('home_teacher/', Home_Teacher, name='home_teacher'),
    path('application_new/', Application_New, name='application_new'),
    path('application_old/', Application_Old, name='application_old'),
]